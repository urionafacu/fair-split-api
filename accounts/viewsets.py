from accounts.models import User
from rest_framework import viewsets
from rules.contrib.rest_framework import AutoPermissionViewSetMixin

from accounts.serializers import UserReadSerializer, UserWriteSerializer
from core.utils.mixins import ReadWriteSerializerMixin

class UserViewSet(AutoPermissionViewSetMixin, ReadWriteSerializerMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    read_serializer_class = UserReadSerializer
    write_serializer_class = UserWriteSerializer
