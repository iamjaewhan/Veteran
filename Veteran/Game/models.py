from django.db import models
from django.utils import timezone
from Account.models import User,Host

#from Auth.models import User,Host

# Create your models here.

class Game(models.Model):
    host=models.ForeignKey('Account.Host',null=False, on_delete=models.PROTECT)
    start_datetime=models.DateTimeField(default=timezone.localtime(), null=False)
    end_datetime=models.DateTimeField(default=timezone.localtime(), null=False)
    numOfRecruitment=models.IntegerField(default=18,null=False)
    completed=models.BooleanField(default=False)

    def changeState(self):
        if self.completed == False:
            self.completed = True
        return self.completed

    def isProcessed(self):
        now_date = datetime.now() 
        game_date = self.start_datetime
    
        result = now_date < game_date
        # 아직 진행 전이면 false 반환
        if result == False:
            self.completed = False
            return self.completed

        # 진행 이후면 True 반환 
        else:
            self.completed = True
            return self.completed


    
    #game.start_datetime datetime형이 맞는지 확인 필요
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
        dictionary["host"] = self.host
        dictionary["start_datetime"] = self.start_datetime
        dictionary["end_datetime"] = self.end_datetime
        dictionary["numOfRecruitment"] = self.numOfRecruitment
        return dictionary
        
        
    
class Game_Participants(models.Model):
    game=models.ForeignKey(Game, on_delete=models.PROTECT)
    user=models.ForeignKey('Account.User', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (('game', 'user'),)
        
    