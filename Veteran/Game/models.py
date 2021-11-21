from django.db import models
import datetime
from django.utils import timezone
from Account.models import User,Host

#from Auth.models import User,Host

# Create your models here.

class Game(models.Model):
    host=models.ForeignKey(Host,null=False, on_delete=models.PROTECT)
    start_datetime=models.DateTimeField(default=timezone.now(), null=False)
    end_datetime=models.DateTimeField(default=timezone.now, null=False)
    numOfRecruitment=models.IntegerField(default=18,null=False)
    completed=models.BooleanField(default=False)
    
class Game_Participants(models.Model):
    game=models.ForeignKey(Game, on_delete=models.PROTECT)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (('game', 'user'),)
    