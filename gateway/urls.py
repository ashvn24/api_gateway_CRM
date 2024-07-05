from django.urls import path
from .views import *

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('user/', UserUpdateRetriveDeleteAPIView.as_view(), name='user'),
    path('book/', BookAPIView.as_view(), name='book'),
]
