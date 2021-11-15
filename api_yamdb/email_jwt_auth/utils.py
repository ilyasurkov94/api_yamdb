import jwt
from datetime import datetime, timedelta
from django.core.mail import send_mail
from random import randint

from api_yamdb.settings import SECRET_KEY
from .models import UserEmailCode


def generate_access_token(user):
    """
    Генерирует веб-токен JSON, в котором хранится идентификатор, срок действия
    потом возьмем с настроек проекта, по умолчанию 1 день от создания
    """
    dt = datetime.utcnow() + timedelta(days=1)
    access_token_payload = {
        'user_id': user.pk,
        'exp': dt
    }
    access_token = jwt.encode(
        access_token_payload,
        SECRET_KEY, algorithm='HS256'
    )
    print(access_token)
    return access_token


def send_mail_confirm_code(username, email):
    """
    Создает новый код подтверждения и отправляет его на почту, при этом удаляет
    старый код подтверждения из базы
    """
    UserEmailCode.objects.filter(username=username, email=email).delete()
    print("send_mail_code")
    confirmation_code = randint(100000, 999999)
    user_email_code = UserEmailCode(
        username=username, email=email,
        confirmation_code=confirmation_code
    )
    user_email_code.save()
    send_mail(
        'Confirmation_code',
        str(confirmation_code),
        'TestServer@example.com',
        (email,),
        fail_silently=False
    )
