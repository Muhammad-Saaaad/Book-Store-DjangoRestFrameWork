from django.db import models
from django.contrib.auth import get_user_model

from seller.models import Book

User = get_user_model()

class Buyer(models.Model):
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null= True)
    book = models.ForeignKey(Book , on_delete=models.SET_NULL , null=True)
    book_quantity = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    is_transaction = models.BooleanField(default=False)