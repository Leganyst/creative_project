
# Определяет функции, которые получают запросы пользователей, обрабатывают их и возвращают ответ
# Create your views here.
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, permissions,  status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, CustomTokenRefreshSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from rest_framework.views import APIView

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    post:
    Создание нового пользователя.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

# class LoginView(TokenObtainPairView):
#     """
#     post:
#     Авторизация пользователя и получение JWT токенов.
#     """
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = LoginSerializer
    
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         # Предполагая, что serializer.validated_data возвращает имя пользователя или другой уникальный идентификатор
#         user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
#         if user is not None:
#             # Получаем токены для пользователя
#             refresh = RefreshToken.for_user(user)
#             access_token = refresh.access_token

#             response_data = {
#                 'refresh': str(refresh),
#                 'access': str(access_token),
#                 'user': UserSerializer(user).data  # Используем сериализатор для преобразования пользователя в JSON
#             }
#             return Response(response_data, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: 'Login successful', 400: 'Bad request'}
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']  # Получаем пользователя напрямую из валидированных данных
        
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        response_data = {
            'refresh': str(refresh),
            'access': str(access_token),
            'user': UserSerializer(user).data 
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

class UserView(generics.RetrieveAPIView):
    """
    get:
    Получение информации о текущем пользователе.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Получение информации о текущем пользователе",
        responses={200: UserSerializer}
    )
    def get_object(self):
        """
        Возвращает объект текущего аутентифицированного пользователя.
        """
        return self.request.user

class CustomTokenRefreshView(TokenRefreshView):
    """
    post:
    Обновление JWT токенов.
    """
    serializer_class = CustomTokenRefreshSerializer