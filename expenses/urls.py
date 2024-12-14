from rest_framework import routers

from expenses.viewsets import ExpenseViewSet, GroupViewSet

router = routers.DefaultRouter()

router.register("expenses", ExpenseViewSet, basename="expense")
router.register("groups", GroupViewSet, basename="group")
