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
    
    def __str__(self):
        return self.email
    
class Review(models.Model):
    reviewer_id=models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    reviewee_id=models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    #한줄평에 사용될 코멘트 입력
    CommentType=[(1,'comment1'),(2,'comment2'),(3,'comment3')]
    comment_type=models.CharField(choices=CommentType, null=False,max_length=30)
    RATING_CHOICES=zip(range(1,6),range(1,6))
    rating=models.IntegerField(choices=RATING_CHOICES)


class Host(models.Model):
    host=models.ForeignKey(User,primary_key=True, on_delete=models.CASCADE)
    court_location=models.CharField(verbose_name='장소',max_length=100, null=False)
    intro=models.CharField(verbose_name='한줄 소개', max_length=200, null=False)
    
    
class HostApplication(models.Model):
    host=models.ForeignKey(User,primary_key=True, on_delete=models.CASCADE)
    court_location=models.CharField(verbose_name='장소',max_length=100, null=False)
    intro=models.CharField(verbose_name='한줄 소개', max_length=200, null=False)
    
    
