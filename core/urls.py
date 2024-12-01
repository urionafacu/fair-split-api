from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from accounts.urls import router as account_router
from accounts.views import LoginView, LogoutView
from expenses.urls import router as expense_router
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.registry.extend(account_router.registry)
router.registry.extend(expense_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
]
