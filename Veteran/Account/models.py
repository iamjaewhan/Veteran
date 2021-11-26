from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(
        verbose_name='닉네임', 
        max_length=15, 
        unique=True, 
        null=False,
        error_messages={'unique': '이미 사용중인 닉네임입니다.'},
    )
    phone = models.CharField(verbose_name='전화 번호', max_length=13,null=False, unique=True,default = '')

    review_relations=models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Review',
        related_name="r")
    
    def __str__(self):
        return self.email
    
class Review(models.Model):
    reviewer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviewing')
    reviewee=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviewed')
    game=models.ForeignKey('Game.Game',on_delete=models.RESTRICT)
    CommentType=[(1,'위험한 플레이를 해요'),(2,'독단적인 플레이를해요'),(3,'이타적인 플레이를 해요'),(4,'실력이 출중한 선수에요'),(5,'매너가 좋은 선수에요')]
    comment_type=models.CharField(choices=CommentType, null=False,max_length=30)
    RATING_CHOICES=zip(range(1,6),range(1,6))
    rating=models.IntegerField(choices=RATING_CHOICES)
    
    class Meta:
        unique_together=(('reviewer','reviewee','game'),)
    

class Host(models.Model):
    host=models.ForeignKey(User,unique=True, on_delete=models.CASCADE)
    group_name=models.CharField(verbose_name='모임 이름',max_length=20, null=False,default='veterans')
    court_location=models.CharField(verbose_name='장소',max_length=100, null=False)
    intro=models.CharField(verbose_name='한줄 소개', max_length=200, null=False)
    
    
class HostApplication(models.Model):
    host=models.ForeignKey(User,unique=True, on_delete=models.CASCADE)
    group_name=models.CharField(verbose_name='모임 이름',max_length=20, null=False,default='veterans')
    court_location=models.CharField(verbose_name='장소',max_length=100, null=False)
    intro=models.CharField(verbose_name='한줄 소개', max_length=200, null=False)
    
    
