from django.db import models

# Create your models here.
class Game(models.Model):
    id=models.IntegerField(primary_key=True)