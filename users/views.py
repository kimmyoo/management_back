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
# load_dotenv()

# authentication
from users.utils.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes

# Create your views here.
# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

class LoginView(APIView):
    permission_classes = [AllowAny]
    # login is post request
    def post(self, request):
        formData = request.data['formData']
        username = formData['username']
        password = formData['password']
        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('User Not Found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')

        # JWT
        payload = {
            'userID': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat': datetime.datetime.utcnow()
        }
        secret = os.environ.get('JWT_SECRET')
        token = jwt.encode(payload, secret, algorithm='HS256')
        response = Response()
        response.set_cookie(
            key='jwt', 
            value=token, 
            httponly=True, 
            samesite='None',  # set this samesite and secure
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
        response.set_cookie('jwt', expires=0, max_age=0, secure=True, samesite='none')
        # response.delete_cookie('jwt') // this doesn't work
        response.data = {
            'message":"logged out'
        }
        return response