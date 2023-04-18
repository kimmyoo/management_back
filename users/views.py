from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserSerializer
#jwt token
import jwt, datetime
from dotenv import load_dotenv
import os
load_dotenv()

# authentication
from users.utils.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    permission_classes = [AllowAny]
    # login is post request
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('User Not Found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')

        # JWT
        payload = {
            'userID': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=3),
            'iat': datetime.datetime.utcnow()
        }
        secret = os.environ.get('JWT_SECRET')
        token = jwt.encode(payload, secret, algorithm='HS256')
        response = Response()
        response.set_cookie(
            key='jwt', 
            value=token, 
            httponly=True, 
            samesite='None',  # set this samesite abd secure
            secure="Secure"  # otherwise the cookie won't be set in browser
        )
        response.data = {'jwt': token}
        return response

@authentication_classes([JWTAuthentication])
class UserView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

@authentication_classes([JWTAuthentication])
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message":"logged out'
        }
        return response