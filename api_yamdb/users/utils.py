from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from api_yamdb.settings import FROM_EMAIL


def send_email_confirmation(user):
    """
    Функция для отправки токена для подверждения учетки.
    """
    token = default_token_generator.make_token(user)
    recipients = []
    recipients.append(user.email)
    send_mail(
        'Ya MDB | Подтверждение учетной записи',
        f'confirmation_code - {token}',
        FROM_EMAIL,
        recipients,
        fail_silently=False,
    )
