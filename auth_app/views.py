from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import Http404
from django.utils import timezone
from rest_framework import status, exceptions, generics, response
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


class LoginView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if not user:
            raise exceptions.AuthenticationFailed()
        user.last_login = timezone.now()
        user.save()

        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        return response.Response(data=data, status=status.HTTP_200_OK)


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserDataView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, _, pk):
        user = User.objects.filter(id=pk).first()
        if not user:
            raise Http404

        serializer = self.get_serializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)
