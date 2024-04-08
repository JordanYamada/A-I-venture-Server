from django.db import models
from django.core import validators as v
from user_app.models import Client
# from item_app.models import Item



# Create your models here.
class Story(models.Model):
    
    theme = models.CharField(
        blank=True,
        null=True,
    )
    role = models.CharField(
        blank=True,
        null=True,
    )
    title = models.CharField(
        default=False,
        blank=True,
        null=True,
    )
    completed = models.BooleanField(
        blank=True,
        null=True,
    )

    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, related_name="stories")