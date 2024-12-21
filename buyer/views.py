from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from seller.models import Shop, Book
from seller.serializer import ShopSerializerShow
from .serializer import BooksSerializerShow , BooksSerializerBuy
from authentication.auth_token import JwtAuthentication


user = get_user_model()

class IsBuyer(BasePermission):
    """_summary_
            authenticating 2nd time to remove any unnecessary access
        Methods:
            check if the user is authenticated or not and the user type must be buyer.
    """
    def has_permission(self, request, view):
        return  request.user.is_authenticated and request.user.user_type =='buyer'

class Shops(APIView):

    """_summary_

    This will first authenticate if this user is authenticated and its a buyer or not

    Methods():
        get(): Shows all the shops
    """
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsBuyer]

    def get(self, request):# there is no serializer validation for get requests
        shop_list = Shop.objects.all()
        serializer = ShopSerializerShow(shop_list , many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class BuyShowBooks(APIView):

    """_summary_

            This class will first authenticate if this user is authenticated and its a buyer or not
        Methods:

            get(): Take the id of shop and display all the books from that shop
            post(): Take book id and quantity of which user wanted to buy, save the data in database return the total price
    """
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsBuyer]
    
    def post(self , request):

        if "book_id" in request.data and 'book_quantity' in request.data:
            
            book = Book.objects.filter(id = request.data["book_id"]).first()

            if book:
                # user_instance = user.objects.filter(id = request.user.id).first()
                quantity = request.data['book_quantity']
                total_price = quantity * book.book_price
                data = {"user":request.user.id, "book":book.id , "book_quantity":quantity , "total_price":total_price}

                serializer = BooksSerializerBuy(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"Message":serializer.data}, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Message":"Book id Invalid"}, status= status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Message":"Book id or quantity not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        if "shop_id" in request.data:
            books_list = Book.objects.filter(shop__id = request.data['shop_id']).all()
            serializer = BooksSerializerShow(books_list, many=True)
            return Response(serializer.data , status=status.HTTP_200_OK)
        else:
            return Response("Shop id not provided", status=status.HTTP_400_BAD_REQUEST)
