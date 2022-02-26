from django.db import models
from django.utils import timezone
from accounts.models import User,Host

#from Auth.models import User,Host

# Create your models here.

class Game(models.Model):
    host = models.ForeignKey('accounts.Host',null=False, on_delete=models.PROTECT)
    start_datetime = models.DateTimeField(default=timezone.localtime(), null=False)
    end_datetime = models.DateTimeField(default=timezone.localtime(), null=False)
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
        
    def toDict(self):
        dictionary = {}
        dictionary['id'] = self.id
        dictionary["host"] = self.host
        dictionary["start_datetime"] = self.start_datetime.strftime("%Y-%m-%d %H:%M")
        dictionary["end_datetime"] = self.end_datetime.strftime("%Y-%m-%d %H:%M")
        dictionary["numOfRecruitment"] = self.numOfRecruitment
        dictionary["numOfParticipation"] = self.numOfParticipation
        return dictionary
    
    def toTuple(self):
        return (
            self.id,
            self.host.group_name,
            self.start_datetime,
            self.end_datetime,
            self.numOfRecruitment,
            self.numOfParticipation
        )
        
        
    
class Game_Participants(models.Model):
    game=models.ForeignKey(Game, on_delete=models.PROTECT)
    user=models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (('game', 'user'),)
        
    def getPlayer(self):
        return [self.user.id, self.user.username]