from accounts.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "password",
            "last_login",
            "user_permissions",
            "is_staff",
            "is_superuser",
            "is_active",
        ]


class UserWriteSerializer(serializers.ModelSerializer):
    pass


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['full_name'] = user.get_full_name()
        token['is_staff'] = user.is_staff

        # Timestamps útiles
        token['created_at'] = str(user.date_joined)
        token['last_login'] = str(user.last_login) if user.last_login else None

        token['groups'] = list(user.groups.values_list('name', flat=True))

        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
