import os
from django.urls import path
from .views.auth import (
    LoginView,
    RefreshTokenView,
    RefreshCheckView,
    LogoutView,
    CurrentUserView
)


app_name = os.getcwd().split(os.sep)[-1]
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("current-user/", CurrentUserView.as_view(), name="current_user"),
    path("refresh-token/", RefreshTokenView.as_view(), name="refresh_token"),
    path("refresh-check/", RefreshCheckView.as_view(), name="refresh_check"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
