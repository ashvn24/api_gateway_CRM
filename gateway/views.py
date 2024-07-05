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
tast_url = os.getenv('TASK_URL')
notification_url = os.getenv('NOTIFICATION_URL')


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
    

class UserUpdateRetriveDeleteAPIView(APIView):
    def get(self, request):
        try:
            token = request.headers.get('Authorization')
            token = str(token)
            payload = decode_jwt(token)
            if not isinstance(payload, dict):
                return Response({'error': payload})
            user_id = payload.get('user_id')
            headers = {'Authorization': token}
            response = requests.get(f'{auth_url}/user/{user_id}/', headers=headers)
            return Response(response.json())
        except Exception as e:
            return Response({'error': str(e)})
    
    def put(self, request):
        try:
            token = request.headers.get('Authorization')
            payload = decode_jwt(token)
            if not isinstance(payload, dict):
                return Response({'error': payload})
            user_id = payload.get('user_id')
            data = request.data
            data_json = json.dumps(data)
            headers = {'Content-Type': 'application/json', 'Authorization': token}
            response = requests.put(f'{auth_url}/user/{user_id}/', data=data_json, headers=headers)
            return Response(response.json())
        except Exception as e:
            return Response({'error': str(e)})
    
    def delete(self, request):
        try:
            token = request.headers.get('Authorization')
            payload = decode_jwt(token)
            if not isinstance(payload, dict):
                return Response({'error': payload})
            user_id = payload.get('user_id')
            headers = {'Authorization': token}
            response = requests.delete(f'{auth_url}/user/{user_id}/', headers=headers)
            return Response({'User deleted successfully'})
        except Exception as e:
            return Response({'error': str(e)})
        
#-------------------------------------------------------Notification------------------------------------------------------------

class NotificationAPIView(APIView):
    
    def get(self, request):
        try:
            token = request.headers.get('Authorization')
            payload = decode_jwt(token)
            if not isinstance(payload, dict):
                return Response({'error': payload})
            headers = {'Authorization': token}
            response = requests.get(f'{notification_url}/notifications/', headers=headers)
            return Response(response.json())
        except Exception as e:
            return Response({'error': str(e)})
        

#-------------------------------------------------------Task------------------------------------------------------------
class BookAPIView(APIView):
    def get(self, request):
        try:
            token = request.headers.get('Authorization')
            payload = decode_jwt(token)
            if not isinstance(payload, dict):
                return Response({'error': payload})
            headers = {'Authorization': token}
            response = requests.get(f'{tast_url}/appointments/', headers=headers)
            return Response(response.json())
        except Exception as e:
            return Response({'error': str(e)})
        
    def post(self, request):
        try:
            token = request.headers.get('Authorization')
            payload = decode_jwt(token)
            if not isinstance(payload, dict):
                return Response({'error': payload})
            user_id = payload.get('user_id')
            data = request.data
            data['user_id'] = user_id 
            
            data_json = json.dumps(data)
            headers = {'Content-Type': 'application/json', 'Authorization': token}
            response = requests.post(f'{tast_url}/appointments/', data=data_json, headers=headers)
            return Response(response.json())
        except Exception as e:
            return Response({'error': str(e)})
        