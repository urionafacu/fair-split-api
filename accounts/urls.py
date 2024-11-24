from rest_framework import routers

from accounts.viewsets import UserViewSet

router = routers.DefaultRouter()

router.register("users", UserViewSet, basename="users")
