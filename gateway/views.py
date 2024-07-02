from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import os
import requests
import jwt,json
from dotenv import load_dotenv


load_dotenv()
# Create your views here.

secret_key = os.getenv('SECRET_KEY')
auth_url = os.getenv('AUTH_URL')


def decode_jwt(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
    except Exception as e:
        return e


class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        data = {'email': email, 'password': password}
        data_json = json.dumps(data)
        headers = {'Content-Type': 'application/json'} 
        response = requests.post(f'{auth_url}/login/', data=data_json, headers=headers)
        return Response(response.json())    


class RegisterAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        data = {'email': email, 'password': password}
        data_json = json.dumps(data)
        headers = {'Content-Type': 'application/json'} 
        response = requests.post(f'{auth_url}/register/', data=data_json, headers=headers)
        return Response(response.json())
    