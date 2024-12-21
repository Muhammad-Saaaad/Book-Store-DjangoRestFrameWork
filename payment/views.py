import os 
import json

import stripe
import stripe.checkout
from dotenv import load_dotenv # pip install python-dotenv
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission

from authentication.views import JwtAuthentication
from .serializer import PaymentSerializer
from buyer.models import Buyer

load_dotenv()
User = get_user_model()

class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        return  request.user.is_authenticated and request.user.user_type =='buyer'

class template_view:

    """_summary_

        for both the url, i have did the following actions:
        1. made a template view class where i have user render from django.shortcuts
        2. before that i have create a templates folder in core folder and then i have 
            given a shortcut in the TEMPLATES dictionary => DIRS
        3. after that i have given the urls in the urls.py file
        4. Then i have just given the links to the cancel_url and success_url
    """

    def sucess_view(request):
        return render(request=request, template_name=r"ThankYou.html")

    def cancel_view(request):
        return render(request=request, template_name=r"cancel.html")

class checkout(APIView):

    """_summary_

        Methods():
            1.post(): 
    """
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsBuyer]
    

    def post(self, request):

        buyer = Buyer.objects.filter(user = request.user.id).first()
        if buyer.is_transaction == False:
            stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
            session = stripe.checkout.Session.create(payment_method_types=['card'],
                line_items=[{
                        'price_data':{
                            'currency':'usd',
                            'product_data':{
                                'name':'Physcology of money',
                                # 'images':[r'https://images.search.yahoo.com/search/images;_ylt=AwrO8p544l9nh1UOK3lXNyoA;_ylu=Y29sbwNncTEEcG9zAzEEdnRpZAMEc2VjA3BpdnM-?p=psychology+of+money&fr2=piv-web&type=E210US91215G0&fr=mcafee#id=1&iurl=https%3A%2F%2Fthethinksync.com%2Fwp-content%2Fuploads%2F2022%2F01%2Fthepsychlogyofmoney.jpg&action=click']
                            },
                            'unit_amount':20000, # cents
                        },
                        'quantity':1,
                    }],
                mode='payment', # you can set the mode on either payment or subsciption
                customer_email=request.user.email,
                payment_intent_data={
                    'metadata':
                            {"user_id":request.user.id , "buyer_id":buyer.id}, 
                },
                success_url=request.build_absolute_uri(reverse("success")),
                cancel_url=request.build_absolute_uri(reverse("cancel"))
            )
            return JsonResponse({"url":session.url,})

@csrf_exempt # disable csrf (Cross-Site Request Forgery) Protection(does not check for csrf token)
def my_webhook_view(request):
    payload = request.body
    event = None
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    # print(sig_header)

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), sig_header,os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except ValueError as e: # invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object # contains a stripe.PaymentIntent

        user_id = payment_intent['metadata']['user_id']
        buyer_id = payment_intent['metadata']['buyer_id']
        # user = User.objects.filter(id = user_id)
        buyer = Buyer.objects.filter(id = buyer_id).first()

        data = {'user':user_id, 'buyer':buyer_id,'total_payment':payment_intent['amount']/100, 
                'paid_payment':payment_intent['amount_received']/100}
        
        # print(payment_intent)
        serializer = PaymentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            buyer.is_transaction = True
            buyer.save()
            print("Payment intent sucessfull")
            return HttpResponse(status=200)
        else:
            print("Payment intent unsucessfull")
            return HttpResponse(status=400)
        
    elif event.type == 'payment_method.attached':
        payment_method = event.data.object # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
        # ... handle other event types
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)

    # stripe listen --forward-to http://127.0.0.1:8000/api-payment/webhooks