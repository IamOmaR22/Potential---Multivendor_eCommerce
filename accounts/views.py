from .serializers import UserSerializers, UserLoginSerializer
from .models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from .permissions import IsAccountType

class AuthUserLoginView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        response = {
            'success': True,
            'message': 'User logged in successfully',
            'token': token.key,
            'username': user.username,
            'user_type': user.user_type,
            'user': UserSerializers(user).data,
        }

        return Response(response, status=status.HTTP_200_OK)


class UserListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAccountType]
    serializer_class = UserSerializers

    def get_queryset(self):
        user = self.request.user

        if user.user_type == User.SELLER:
            queryset = User.objects.filter(user_type=User.BUYER)
        elif user.user_type == User.BUYER:
            queryset = User.objects.filter(user_type=User.SELLER)
        else:
            queryset = User.objects.all()

        return queryset


class EachUserDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsAccountType]
    serializer_class = UserSerializers
    queryset = User.objects.all()


class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializers


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAccountType]
    serializer_class = UserSerializers
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if 'password' in request.data:
            serializer.validated_data['password'] = make_password(request.data['password'])

        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAccountType]
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success": True, "message": "User deleted successfully"}, status=status.HTTP_200_OK)
