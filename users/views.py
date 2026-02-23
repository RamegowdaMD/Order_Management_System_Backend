from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserRegistrationSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

class LoginView(TokenObtainPairView):
    pass
