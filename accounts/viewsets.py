from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rules.contrib.rest_framework import AutoPermissionViewSetMixin

from accounts.models import User
from accounts.serializers import UserReadSerializer, UserWriteSerializer
from core.utils.mixins import ReadWriteSerializerMixin


class UserViewSet(
    AutoPermissionViewSetMixin, ReadWriteSerializerMixin, viewsets.ModelViewSet
):
    queryset = User.objects.all()
    read_serializer_class = UserReadSerializer
    write_serializer_class = UserWriteSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return super().get_permissions()
