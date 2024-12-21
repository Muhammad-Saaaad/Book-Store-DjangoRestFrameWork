import random

from django.core.mail import send_mail
from core.settings import EMAIL_HOST_USER

def create_otp():
    return random.randint(100000,999999)

def send_otp_mail(email, otp):
    subject = 'Book store SignUp'
    message=f'Your otp for book store registration is {otp}'
    sender_email = EMAIL_HOST_USER
    recipient_email = [email]
    send_mail(subject=subject, message=message, from_email=sender_email, recipient_list= recipient_email)

def otp_change_password(email, otp):
    subject = 'Book store'
    message = f'your otp for change password is {otp}'
    sender_mail = EMAIL_HOST_USER
    recipient_mail = [email]
    send_mail(subject=subject, message=message, from_email=sender_mail, recipient_list=recipient_mail)