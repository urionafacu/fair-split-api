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
    updated_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50, choices=GROUP_CHOICES)


class GroupMember(models.Model):
    ROLE_CHOICES = [
        ("ADMIN", "Admin"),
        ("MEMBER", "Member"),
    ]
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ["group", "user"]
