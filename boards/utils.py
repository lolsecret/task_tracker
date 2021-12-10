from django.core.mail import send_mail
from django.conf import settings

from task_tracker import celery_app
from requests.exceptions import ConnectionError, HTTPError, Timeout, ReadTimeout


@celery_app.task(
    autoretry_for=(ConnectionError, HTTPError, Timeout),
    default_retry_delay=2,
    retry_kwargs={"max_retries": 5},
    ignore_result=True,
)
def send_email(subject, text, to_mail):
    print('ya tut')
    send_mail(
        subject,
        text,
        settings.EMAIL_HOST_USER,
        to_mail,
        fail_silently=False,
    )
    return True