from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken import views
from . import views
from .views import ResetPasswordEmailApiView,PasswordTokenCheckApi



urlpatterns = [
    path("register",views.register,name="register"),
    path("login",views.login,name="login"),
    path("Reset_pass_Request_email",views.Reset_pass_Request_email,name="Reset_pass_Request_email"),
    path("logout",views.logout,name="logout"),
    path('request-reset-email/', ResetPasswordEmailApiView.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckApi.as_view(), name='password-reset-confirm'),
]