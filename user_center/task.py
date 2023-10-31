from fresh_shop import settings
from django.core.mail import send_mail
from celery.task import task


@task
def send_verify_email(title, email, html_message):
    """
    发送验证邮件
    :param title:
    :param email:
    :param html_message:
    :return:
    """
    send_mail(title, '', settings.EMAIL_FROM, [email], html_message=html_message)

