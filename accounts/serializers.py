from django.contrib.auth.models import make_password
from django.db import transaction
from rest_framework import serializers

from accounts.models import User
from expenses.models.group import Group, GroupMember


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
    partner_first_name = serializers.CharField(write_only=True, required=True)
    partner_last_name = serializers.CharField(write_only=True, required=True)
    partner_email = serializers.EmailField(write_only=True, required=True)
    partner_income = serializers.DecimalField(
        write_only=True,
        required=True,
        max_digits=12,
        decimal_places=2,
        min_value=0,
    )
    income = serializers.DecimalField(
        write_only=True,
        required=True,
        max_digits=12,
        decimal_places=2,
        min_value=0,
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "income",
            "partner_first_name",
            "partner_last_name",
            "partner_email",
            "partner_income",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_partner_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this partner email already exists."
            )
        return value

    def create(self, validated_data):
        with transaction.atomic():
            partner_first_name = validated_data.pop("partner_first_name")
            partner_last_name = validated_data.pop("partner_last_name")
            partner_email = validated_data.pop("partner_email")
            partner_income = validated_data.pop("partner_income")
            income = validated_data.pop("income")

            # Create main user
            user = User.objects.create_user(
                email=validated_data.get("email", ""),
                password=validated_data.get("password", ""),
                first_name=validated_data.get("first_name", ""),
                last_name=validated_data.get("last_name", ""),
            )

            # Create partner user (inactive)
            partner_user = User.objects.create_user(
                email=partner_email,
                password=make_password(None),  # random unusable password
                first_name=partner_first_name,
                last_name=partner_last_name,
                is_active=False,
            )

            # Create group of type Couple
            group = Group.objects.create(type=Group.COUPLE)

            # Create GroupMember for main user
            GroupMember.objects.create(
                group=group,
                user=user,
                income=income,
                income_currency="ARS",
                income_frequency=GroupMember.MONTHLY,
                role=GroupMember.ADMIN,
            )

            # Create GroupMember for partner
            GroupMember.objects.create(
                group=group,
                user=partner_user,
                income=partner_income,
                income_currency="ARS",
                income_frequency=GroupMember.MONTHLY,
                role=GroupMember.MEMBER,
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
