from django.db import models
from django.contrib.auth import get_user_model

from buyer.models import Buyer

User = get_user_model()

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL , null=True)
    buyer = models.ForeignKey(Buyer , on_delete=models.SET_NULL, null=True)
    total_payment = models.FloatField()
    paid_payment = models.FloatField()