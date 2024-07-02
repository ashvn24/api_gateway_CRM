from django.urls import path
from .views import *

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
]
