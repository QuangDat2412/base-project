import os
from django.urls import path, include

app_name = os.getcwd().split(os.sep)[-1]

urlpatterns = (
    path("auth/", include("modules.users.urls", namespace="auth")),
)
