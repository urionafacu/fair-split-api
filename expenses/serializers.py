from rest_framework import serializers
from .models import Group, GroupMember, Expense

class ExpenseReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"

class ExpenseWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"
