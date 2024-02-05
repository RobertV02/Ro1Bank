from django.db import models
from django.contrib.auth.models import User

class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2)

class Check(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
