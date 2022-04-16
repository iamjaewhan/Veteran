from django.db import models
from django.utils import timezone
from accounts.models import User,Host

#from Auth.models import User,Host

# Create your models here.

class Game(models.Model):
    host = models.OneToOneField(Host, null=False, on_delete=models.PROTECT)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    numOfRecruitment = models.IntegerField(default=18,null=False)
    numOfParticipation = models.IntegerField(default=0,null=False)
    completed = models.BooleanField(default=False)
    
    
    def isProgressed(self):
        if self.start_datetime>timezone.localtime():
            return False
        else:
            return True
        
    def updateState(self):
        if self.isProgressed():
            self.completed=True
        return True
    
class HostGame(models.Model):
    host = models.ForeignKey(Host, on_delete = models.PROTECT)
    game = models.ForeignKey(Game, on_delete = models.PROTECT)
        

    
class Game_Participant(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (('game', 'user'),)
        
    def getPlayer(self):
        return [self.user.id, self.user.username]