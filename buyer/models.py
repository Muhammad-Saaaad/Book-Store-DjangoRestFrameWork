from django.db import models
from django.contrib.auth import get_user_model

from seller.models import Shop , Book

User = get_user_model()

class Buyer(models.Model):
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null= True)
    book = models.ForeignKey(Book , on_delete=models.SET_NULL , null=True)
    book_quantity = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    is_transaction = models.BooleanField(default=False)

# class CartBooks(models.Model):
#     book_name = models.CharField(max_length=50)
#     book_discription= models.CharField(max_length=100)
#     book_price = models.FloatField()
#     book_quantity = models.IntegerField()

# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     item = models.ForeignKey(CartBooks, on_delete=models.CASCADE)