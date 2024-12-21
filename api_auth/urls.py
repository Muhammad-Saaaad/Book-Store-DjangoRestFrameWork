from django.urls import path

from authentication.views import *

urlpatterns = [
    path('Register-get-otp', Registration.as_view()),
    path('Confirm-Registration', RegistrationConfirm.as_view()),
    path('User-Crud', UserDelete.as_view()),
    path('Admin-only',AdminOnly.as_view()),
    path('login', Login.as_view()),
    path('change-password/send-otp', ChangePasswordOtp.as_view()),
    path('Confirm-otp', ConfirmOtp.as_view()),
    path('change-password/confirm-Password', ConfirmNewPassowrd.as_view())
]