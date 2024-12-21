from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission # when you want to make your own premissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated # use when you are using django self token

from .models import *
from .serializer import *
from authentication.auth_token import JwtAuthentication

class IsSeller(BasePermission):
    """_summary_
            authenticating 2nd time to remove any unnecessary access
        Methods:
            check if the user is authenticated or not and the user type must be seller.
    """ 
    def has_permission(self, request, view):
        return  request.user.is_authenticated and request.user.user_type =='seller'

# class ShopView(ModelViewSet):
#     authentication_classes = [JwtAuthentication]
#     permission_classes = [IsSeller]

#     queryset = Shop.objects.all()
#     serializer_class = ShopSerializer

    # def list(self, request):

class ShopView(APIView):

    """
        check JWT Token authentication along with if the user is a seller or not.
        Methods:
            1. post(): take the shop data from user along with user id and then make the shop. 
            (it does not take any user requirements rather it extract from the JWT token)
            2. get(): show all the shops of only the user who is hitting the request
            3. delete(): get a shop id and delete that shop
    """

    authentication_classes = [JwtAuthentication]
    permission_classes = [IsSeller]

    def post(self , request):
        data : dict= request.data
        user_id = request.user.id
        data.update({"user":user_id})
        serializer = ShopSerializerInsert(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Shop added"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self , request): # user can only see his shops
        shop = Shop.objects.filter(user__id = request.user.id).all()
        serializer= ShopSerializerShow(shop , many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        shop = Shop.objects.filter(id = request.data['id']).first()
        shop.delete()
        return Response({"message":"Shop deleted sucessfully"}, status=status.HTTP_204_NO_CONTENT)

class BookView(APIView):

    """_summary_

        Methods():
            1.post(): 1st it will check weather the shop(shop name) is in the request.data or not
                      if it is, then it will get the use id add into the data then from shop name it will 
                      get shop id add into the data make a serializer of the data and add the data to Book Table.
                    
            2. get(): Show only the books, that seller has added to database. 
            3. patch(): Take the book id and change the required data.
            4. delete(): Seller will only give the book name 
    """

    authentication_classes = [JwtAuthentication]
    permission_classes = [IsSeller]

    def post(self , request):
        if "shop" in request.data:
            data = request.data
            data.update({"user":request.user.id})
            shop = Shop.objects.filter(shop_name=request.data["shop"]).first()
            if shop:
                if shop.user.id == request.user.id: # checking if the shop owner is adding the book or anyother
                    data.update({"shop":shop.id})
                    serializer = BookSerializerInsert(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({"message":"book inserted sucessfully"}, status= status.HTTP_201_CREATED)
                    else:
                        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message":"You does not own this shop"},status= status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"shop does not exists"},status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Shop name not provided"})
        
    def get(self, request):
        books = Book.objects.filter(user__id = request.user.id).all()
        serializer = BookSerializerGetDelete(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, requst):
        book = Book.objects.filter(id = requst.data['id']).first()
        serializer = BookSerializerInsert(book, requst.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"data saved sucessfully"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request): # Enter book name
        # get the book name and delete that book name, follow by if the user has published that book or not
        if "book_name" in request.data:
            book = Book.objects.filter(book_name = request.data["book_name"])
            if book: # if book exists then delete it
                if book.user.id == request.user.id:
                    book.delete()
                    return Response({"message":"Book deleted sucessfully"}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"messsage":"User has not published this book"},status=status.HTTP_400_BAD_REQUEST)
            else:
                    return Response({"messsage":"Book does not exists"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"messsage":"Enter book_name"},status=status.HTTP_400_BAD_REQUEST)
