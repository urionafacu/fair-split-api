from django.contrib import admin

from expenses.models import Expense, Group, GroupMember

admin.site.register(Expense)
admin.site.register(Group)
admin.site.register(GroupMember)
