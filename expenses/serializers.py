from rest_framework import serializers

from accounts.models.user import User
from .models import Group, GroupMember, Expense

class ExpenseReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"

class ExpenseWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"


class GroupMemberUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class GroupMemberSerializer(serializers.ModelSerializer):
    user = GroupMemberUserSerializer()

    class Meta:
        model = GroupMember
        fields = ['id', 'user', 'role', 'joined_at']

class GroupSerializer(serializers.ModelSerializer):
    members = GroupMemberSerializer(many=True)

    class Meta:
        model = Group
        fields = ['id', 'type', 'created_at', 'members']
