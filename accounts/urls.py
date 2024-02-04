from django.urls import path
from .views import (
    UserListAPIView,
    AuthUserLoginView,
    UserCreateAPIView,
    UserUpdateView,
    UserDeleteView,
    EachUserDetailView
)

urlpatterns = [
    path('user/create/', UserCreateAPIView.as_view(), name='user-create'),
    path('user/', UserListAPIView.as_view(), name='user-list'),
    path('user/<int:pk>/', EachUserDetailView.as_view(), name='user-detail'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('login/', AuthUserLoginView.as_view(), name='login'),
]
