# authentication.py
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from ..models import User
from dotenv import load_dotenv
import os
load_dotenv()


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = self.get_token(request)
        if token is None:
            raise AuthenticationFailed('unauthenticated')
        try:
            secret = os.environ.get('JWT_SECRET')
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            user = User.objects.get(id=payload['userID'])
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            raise AuthenticationFailed('Invalid or expired token.')
        return (user, token)

    def get_token(self, request):
        # Extract token from request cookies
        token = None
        if not token:
            token = request.COOKIES.get('jwt')
        return token

    # def authenticate_header(self, request):
    #     return 'Bearer'

