from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView


@throttle_classes([UserRateThrottle])
@permission_classes([AllowAny])
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        user = authenticate(email=email, password=password)

        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


@throttle_classes([UserRateThrottle])
@permission_classes([AllowAny])
class LogoutView(APIView):
    def post(self, request):
        logout(request)

        return Response(status=status.HTTP_200_OK)
