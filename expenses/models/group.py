from django.db import models
from django.conf import settings

class Group(models.Model):
    COUPLE = "Couple"
    FAMILY = "Family"
    FRIENDS = "Friends"
    GROUP_CHOICES = [
        (COUPLE, COUPLE),
        (FAMILY, COUPLE),
        (FRIENDS, COUPLE),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=50, choices=GROUP_CHOICES)


class GroupMember(models.Model):
    ADMIN = "Admin"
    MEMBER = "Member"
    ROLE_CHOICES = [
        (ADMIN, ADMIN),
        (MEMBER, MEMBER),
    ]
    MONTHLY = "Monthly"
    BIWEEKLY = "Bi-weekly"
    WEEKLY = "Weekly"
    YEARLY = "Yearly"
    INCOME_FREQUENCY_CHOICES = [
        (MONTHLY, MONTHLY),
        (BIWEEKLY, BIWEEKLY),
        (WEEKLY, WEEKLY),
        (YEARLY, YEARLY),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    income_currency = models.CharField(max_length=3, default="ARS")
    income_frequency = models.CharField(max_length=20, choices=INCOME_FREQUENCY_CHOICES, default=MONTHLY)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ["group", "user"]
