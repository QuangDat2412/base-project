import contextlib
from django.contrib.auth.hashers import make_password, check_password
from modules.users.helper.sr import UserSr
from service.framework_service import _
from service.error_service import ErrorService
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse
from service.request_service import RequestService
from service.token_service import TokenService

User = get_user_model()


class CurrentUserView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        res = UserSr(request.user)
        return RequestService.res(res.data)
    
class LoginView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        error_message = _("Incorrect login information. Please try again")
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            tokens = TokenService.get_token_from_username(user)
            response = JsonResponse(tokens)
            TokenService.set_token_cookie(response, str(tokens['access_token']))
            TokenService.set_refresh_token_cookie(response, str(tokens['refresh_token']))
            return response;
        else:
            ErrorService.validation_error(str(error_message))

class RefreshTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")
        token = TokenService.refresh(refresh_token)
        if not token:
            error_message = _("Can not refresh token")
            return RequestService.err(error_message)
        return RequestService.res({'refresh_token': refresh_token,
                'access_token':token,})


class RefreshCheckView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return RequestService.res({})


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        with contextlib.suppress(Exception):
            token = TokenService.get_token_from_headers(request.headers, False)
            user = TokenService.get_user_from_token(token)
            user.refresh_token_signature = ""
            user.save()
        return RequestService.res({})

