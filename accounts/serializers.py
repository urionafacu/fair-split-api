from accounts.models import User
from rest_framework import serializers


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
