from django.db import models
from django.core import validators as v
from user_app.models import Client




# Create your models here.
class Memory(models.Model):
    
    image = models.CharField(
        blank=True,
        null=True,
    )
    dialogue = models.CharField(
        blank=True,
        null=True,
    )
    title = models.CharField(
        blank=True,
        null=True,
    )

    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, related_name="memories")