from django.contrib.auth.models import User
from django.db import models

class Debt(models.Model):
    payer = models.ForeignKey(User,related_name='payer')
    payee = models.ForeignKey(User,related_name='payee')
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    memo = models.TextField()
    
    
