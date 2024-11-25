from rest_framework import routers

from expenses.viewsets import ExpenseViewSet

router = routers.DefaultRouter()

router.register("expenses", ExpenseViewSet, basename="expenses")
