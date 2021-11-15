from rest_framework import serializers, status

from .models import User
from email_jwt_auth.exceptions import CustomValidation


class UserSerializer(serializers.ModelSerializer):
    """Описание не придумал"""
    email = serializers.EmailField(max_length=254, required=True)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(required=False)
    role = serializers.ChoiceField(choices=['user', 'moderator', 'admin'],
                                   required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name',
                  'last_name', 'bio', 'role']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise CustomValidation("Такая почта уже существует!", 'email',
                                   status_code=status.HTTP_400_BAD_REQUEST)
        return value

    def validate_role(self, value):
        if self.partial:
            request = self.context.get('request')
            user = request.user
            if not (user.is_admin or user.is_superuser):
                if request and hasattr(request, "user"):
                    if user.is_user:
                        return "user"
                    elif user.is_moderator:
                        return "moderator"
        return value
