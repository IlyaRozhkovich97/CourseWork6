import smtplib
import logging
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail
from mailing.models import Mailing, Log, Message
from django.core.cache import cache
from config.settings import CACHE_ENABLED

logger = logging.getLogger(__name__)


def send_mailing():
    """
    Функция отправки рассылок
    """
    logger.debug("send_mailing function called")
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.filter(status__in=[Mailing.STARTED, Mailing.CREATED])

    if not mailings:
        logger.debug("No mailings to process")

    for mailing in mailings:
        logger.debug(f"Processing mailing: {mailing.id}")
        logger.debug(f"Current datetime: {current_datetime}, mailing end_date: {mailing.end_date}")

        # Если достигли end_date, завершить рассылку
        if mailing.end_date and current_datetime >= mailing.end_date:
            mailing.status = Mailing.COMPLETED
            mailing.save()
            logger.debug(f"Mailing {mailing.id} completed due to end_date.")
            continue  # Пропустить отправку, если end_date достигнут

        # Проверить, нужно ли отправить сообщение в текущий момент времени
        logger.debug(f"Mailing next_send_time: {mailing.next_send_time}")
        if mailing.next_send_time and current_datetime >= mailing.next_send_time:
            mailing.status = Mailing.STARTED
            clients = mailing.clients.all()
            logger.debug(f"Clients to send: {[client.email for client in clients]}")

            if not clients:
                logger.debug(f"No clients for mailing {mailing.id}")
                continue

            try:
                logger.debug("Sending mail with following details:")
                logger.debug(f"Subject: {mailing.message.title}")
                logger.debug(f"Message: {mailing.message.message}")
                logger.debug(f"From: {settings.EMAIL_HOST_USER}")
                logger.debug(f"To: {[client.email for client in clients]}")

                server_response = send_mail(
                    subject=mailing.message.title,
                    message=mailing.message.message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in clients],
                    fail_silently=False,
                )
                logger.debug(f"Mail sent successfully: {server_response}")
                Log.objects.create(status=Log.SUCCESS,
                                   server_response=server_response,
                                   mailing=mailing)
            except smtplib.SMTPException as e:
                logger.error(f"Mail sending failed: {str(e)}")
                Log.objects.create(status=Log.FAIL,
                                   server_response=str(e),
                                   mailing=mailing)

            # Обновление времени следующей отправки
            if mailing.periodicity == Mailing.DAILY:
                mailing.next_send_time += timedelta(days=1)
            elif mailing.periodicity == Mailing.WEEKLY:
                mailing.next_send_time += timedelta(weeks=1)
            elif mailing.periodicity == Mailing.MONTHLY:
                mailing.next_send_time += timedelta(days=30)

            mailing.save()
            logger.debug(f"Mailing {mailing.id} next_send_time updated to {mailing.next_send_time}")


def start_scheduler():
    logger.debug("Starting scheduler...")
    scheduler = BackgroundScheduler()
    # Проверка, добавлена ли задача уже
    if not scheduler.get_jobs():
        logger.debug("Adding job to scheduler...")
        scheduler.add_job(send_mailing, 'interval', seconds=30)

    if not scheduler.running:
        scheduler.start()
        logger.debug("Scheduler started")


def get_messages_from_cache():
    """
    Получение списка сообщений из кэша. Если кэш пуст,то получение из БД.
    """
    if not CACHE_ENABLED:
        return Message.objects.all()
    else:
        key = 'categories_list'
        messages = cache.get(key)
        if messages is not None:
            return messages
        else:
            messages = Message.objects.all()
            cache.set(key, messages)
            return messages
