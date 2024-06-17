from django.urls import path
from .views import RegisterView, LoginView, UserView, CustomTokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
