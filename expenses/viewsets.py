from rest_framework import viewsets
from rules.contrib.rest_framework import AutoPermissionViewSetMixin
from core.utils.mixins import ReadWriteSerializerMixin
from .models import Expense
from .serializers import ExpenseReadSerializer, ExpenseWriteSerializer

class ExpenseViewSet(AutoPermissionViewSetMixin, ReadWriteSerializerMixin, viewsets.ModelViewSet):
    read_serializer_class = ExpenseReadSerializer
    write_serializer_class = ExpenseWriteSerializer

    def get_queryset(self):
        return Expense.objects.filter(
            group__members__user=self.request.user
        ).select_related('group').distinct()
