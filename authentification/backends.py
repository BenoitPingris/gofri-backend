import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions


class JWTAuthentification(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None
        prefix, token = auth_data('utf-8').split(' ')
        try:
            payload = jwt.decode(token, settings.JWT_SECRET)
            user = User.objects.get(username=payload['username'])
            return (user, token)
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Your token is not valid.')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Your token has expired.')
        return super().authenticate(request)
