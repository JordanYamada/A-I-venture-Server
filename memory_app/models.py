from django.db import models
from django.core import validators as v




# Create your models here.
class Progress(models.Model):
    
    image = models.CharField(
        blank=True,
        null=True,
    )
    dialogue = models.CharField(
        blank=True,
        null=True,
    )
    # choice_one = models.CharField(
    #     blank=True,
    #     null=True,
    # )
    # choice_two = models.CharField(
    #     blank=True,
    #     null=True,
    # )
    # choice_three = models.CharField(
    #     blank=True,
    #     null=True,
    # )
