from django.db import models
from rules import is_authenticated
from rules.contrib.models import RulesModelBase, RulesModelMixin
from django.utils.translation import gettext_lazy as _

class Expense(RulesModelMixin, models.Model, metaclass=RulesModelBase):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="expenses")

    class Meta:
        verbose_name = _("expense")
        verbose_name_plural = _("expenses")
        rules_permissions = {
            "add": is_authenticated,
            "view": is_authenticated,
            "change": is_authenticated,
            "delete": is_authenticated,
        }
