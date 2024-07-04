import smtplib
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail
from mailing.models import Mailing, Log, Message
from django.core.cache import cache
from config.settings import CACHE_ENABLED


def send_mailing():
    """
    Функция отправки рассылок
    """
    print("send_mailing function called")  # Debug message
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.filter(status__in=[Mailing.STARTED, Mailing.CREATED])

    for mailing in mailings:
        print(f"Processing mailing: {mailing.id}")  # Debug message
        # Если достигли end_date, завершить рассылку
        if mailing.end_date and current_datetime >= mailing.end_date:
            mailing.status = Mailing.COMPLETED
            mailing.save()
            continue  # Пропустить отправку, если end_date достигнут

        # Проверить, нужно ли отправить сообщение в текущий момент времени
        if mailing.next_send_time and current_datetime >= mailing.next_send_time:
            mailing.status = Mailing.STARTED
            clients = mailing.clients.all()
            try:
                server_response = send_mail(
                    subject=mailing.message.title,
                    message=mailing.message.message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in clients],
                    fail_silently=False,
                )
                print(f"Mail sent successfully: {server_response}")  # Debug message
                Log.objects.create(status=Log.SUCCESS,
                                   server_response=server_response,
                                   mailing=mailing, )
            except smtplib.SMTPException as e:
                print(f"Mail sending failed: {str(e)}")  # Debug message
                Log.objects.create(status=Log.FAIL,
                                   server_response=str(e),
                                   mailing=mailing, )

            # Обновление времени следующей отправки
            if mailing.periodicity == Mailing.DAILY:
                mailing.next_send_time += timedelta(days=1)
            elif mailing.periodicity == Mailing.WEEKLY:
                mailing.next_send_time += timedelta(weeks=1)
            elif mailing.periodicity == Mailing.MONTHLY:
                mailing.next_send_time += timedelta(days=30)

            mailing.save()


def start_scheduler():
    print("Starting scheduler...")  # Debug message
    scheduler = BackgroundScheduler()
    # Проверка, добавлена ли задача уже
    if not scheduler.get_jobs():
        print("Adding job to scheduler...")  # Debug message
        scheduler.add_job(send_mailing, 'interval', seconds=30)

    if not scheduler.running:
        scheduler.start()
        print("Scheduler started")  # Debug message


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


# Test function to check email sending manually
def test_send_mail():
    try:
        server_response = send_mail(
            subject="Test Email",
            message="This is a test email.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["your_test_email@example.com"],  # Replace with your test email
            fail_silently=False,
        )
        print(f"Test mail sent successfully: {server_response}")
    except smtplib.SMTPException as e:
        print(f"Test mail sending failed: {str(e)}")


# Ensure the scheduler starts when the server starts
if __name__ == "__main__":
    start_scheduler()
    test_send_mail()
