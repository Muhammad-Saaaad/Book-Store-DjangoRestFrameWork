from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Shop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=40)

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=50)
    book_discription= models.CharField(max_length=100)
    book_price = models.FloatField()
    book_quantity = models.IntegerField()