import os
import smtplib

import django
from django.core.mail import send_mail
from django.conf import settings

# Установите переменную окружения для файла настроек
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Настройте Django
django.setup()


def test_send_mail():
    try:
        server_response = send_mail(
            subject="Тестовое электронное письмо",
            message="Это тестовое электронное письмо.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["solod-spb78@yandex.ru"],  # Замените на ваш тестовый email
            fail_silently=False,
        )
        print(f"Тестовое письмо отправлено успешно: {server_response}")
    except smtplib.SMTPException as e:
        print(f"Не удалось выполнить тестовую отправку : {str(e)}")


# Вызовите функцию для тестирования отправки письма
if __name__ == "__main__":
    test_send_mail()
