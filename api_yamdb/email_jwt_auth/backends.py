import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    """Пишем собственный бэкенд аутентификации"""

    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        """Возвращаем None если не хотим, (user, token) если хотим"""
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefixx = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefixx:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """Попытка аутентификации с предоставленными данными"""
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
        except Exception:
            msg = 'Ошибка аутентификации, невозможно декодировать токен.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['user_id'])
        except User.DoesNotExist:
            msg = "Пользователь соответствующий данному токену не найден."
            raise exceptions.AuthenticationFailed(msg)
        return (user, token)
