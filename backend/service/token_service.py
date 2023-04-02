from typing import Union
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from service.framework_service import get_user_model
from custom_type import query_obj
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from service.date_service import DateService

User = get_user_model()


class TokenService:
    @staticmethod
    def get_token_from_headers(headers: dict, is_jwt=True):
        prefix = "JWT " if is_jwt else "Bearer "
        full_token = headers.get("Authorization")
        if not full_token:
            return ""
        token_arr = full_token.split(" ")
        if len(token_arr) != 2:
            return ""
        prefix = token_arr[0]
        token = token_arr[1]
        return "" if not token or prefix not in ["Bearer", "JWT"] else token

    @staticmethod
    def get_token_signature(token: str) -> str:
        return token.split(".")[-1]

    @staticmethod
    def refresh(refresh_token: str) -> str:
        try:
            return str(RefreshToken(refresh_token).access_token)
        except Exception:  # skipcq: whatever error
            return ""

    @staticmethod
    def generate(user: query_obj) -> Union[query_obj, None]:
        refresh = RefreshToken.for_user(user)
        data = {
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
        }
        return data

    @staticmethod
    def get_token_from_username(username: query_obj) -> Union[query_obj, None]:        
        try:
            return TokenService.generate(username)
        except Exception:
            return ""

    @staticmethod
    def get_user_from_token(token: str) -> Union[query_obj, None]:
        try:
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)     
            return jwt_auth.get_user(validated_token)
        except Exception as e:  # skipcq: whatever error
            return None
        
    @staticmethod
    def set_token_cookie(response, access_token):
        response.set_cookie(
            key=settings.SIMPLE_JWT['TOKEN_COOKIE_NAME'],
            value=access_token,
            expires=DateService.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            httponly=True,
        )

    @staticmethod
    def set_refresh_token_cookie(response, refresh_token):
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            expires=DateService.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            httponly=True,
        )



