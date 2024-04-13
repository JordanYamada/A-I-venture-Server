from django.db import models
from django.core import validators as v




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