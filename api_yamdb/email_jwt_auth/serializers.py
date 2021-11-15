from rest_framework import serializers, status


from .models import UserEmailCode, User
from .utils import generate_access_token, send_mail_confirm_code
from .exceptions import CustomValidation


class UserRegistrationsSerializer(serializers.ModelSerializer):
    """Для регистрации или получения кода на почту"""
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'username']

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if username == 'me':
            raise serializers.ValidationError('Нельзя использовать такой ник!')

        new_user_flag = True

        if User.objects.filter(username=username, email=email).exists():
            # только отправляем код без создания нового пользователя
            new_user_flag = False
        elif User.objects.filter(username=username):
            # такой пользователь уже есть под другой почтой
            raise serializers.ValidationError(
                'Пользователь с таким username существует!')
        elif User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'На эту почту зареган другой username')
        # А если свободный ник, свободная почта отправляем код на почту
        # и возвращаем пользователя
        send_mail_confirm_code(username, email)
        if new_user_flag:
            return data
        raise serializers.ValidationError(
            'Код подтверждения отправлен на почту!')


class UserEmailCodeSerializer(serializers.ModelSerializer):
    """
    Для получения токена при отправке username и code
    При успешной авторизации старый код подтверждения удаляется
    """

    username = serializers.SlugField(required=True)
    confirmation_code = serializers.IntegerField(required=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = UserEmailCode
        fields = ['username', 'confirmation_code', 'token']
        extra_kwargs = {
            'username': {'write_only': True},
            'confirmation_code': {'write_only': True}
        }

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise CustomValidation(
                "Нет такого юзера", 'username',
                status_code=status.HTTP_404_NOT_FOUND
            )
        return value

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        user = User.objects.get(username=username)

        user_email_code = UserEmailCode.objects.filter(
            username=user.username,
            confirmation_code=confirmation_code,
            email=user.email
        )
        if user_email_code:
            # должны выдать ему токен и удалить использованный код
            user_email_code.delete()
            token = generate_access_token(user=user)
            data['token'] = token
            return data
        raise serializers.ValidationError("Неправильная пара")
