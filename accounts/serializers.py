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
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


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
