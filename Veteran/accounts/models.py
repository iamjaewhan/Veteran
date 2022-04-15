from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core import serializers
from django.core.validators import RegexValidator


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, nickname, phone, password=None):
        if not email:
            raise ValueError(_("사용자는 이메일 주소를 필수로 입력해야 합니다."))
        if not nickname:
            raise ValueError(_('사용자는 사용자명을 필수로 입력해야 합니다.'))
        if not phone:
            raise ValueError(_('사용자는 전화번호를 필수로 입력해야 합니다.'))
        
        user = self.model(
            email = self.normalize_email(email),
            nickname = nickname,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, nickname, phone, password=None):
        user = self.create_user(
            email = email,
            nickname = nickname,
            phone = phone,
            password = password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using = self._db)
        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique = True,
        null = False,
        default = False,
        max_length = 100,
        )
    
    nickname = models.CharField(
        verbose_name = '닉네임', 
        max_length = 15, 
        unique = True, 
        null = False,
        error_messages = {'unique': '이미 사용중인 닉네임입니다.'},
        )
    
    phoneNumberRegex = RegexValidator(regex = r"^01([0|1|6|7|8|9])-?([1-9][0-9]{2,3})-?([0-9]{4})$")
    
    phone = models.CharField(
        verbose_name = '전화 번호',
        validators = [phoneNumberRegex],
        max_length = 13,
        null = False,
        unique = False,
        )
    
    is_host = models.BooleanField(
        null=False,
        default=False
        )
    
    is_superuser = models.BooleanField(
        null = False,
        default = False,
        )
    
    is_staff = models.BooleanField(
        null = False,
        default = False,
        )
    
    review_relations = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Review',
        related_name="r",
        )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone','nickname']
    
    objects = UserManager()
    
    def __str__(self):
        return self.nickname
    
class Review(models.Model):
    reviewer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviewing')
    reviewee = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviewed')
    comment = models.CharField(verbose_name = '평가', max_length = 100, null = True)
    RATING_CHOICES = zip(range(1,6),range(1,6))
    rating = models.IntegerField(choices=RATING_CHOICES)
    
    class Meta:
        unique_together=(('reviewer','reviewee'),)
        

class Host(models.Model):
    host = models.ForeignKey(User, unique=False , on_delete=models.CASCADE)
    group_name = models.CharField(verbose_name='모임 이름',max_length=20, null=False,default='veterans')
    court_location = models.CharField(verbose_name='장소',max_length=100, null=False)
    intro = models.CharField(verbose_name='한줄 소개', max_length=200, null=False)
    
    def __str__(self):
        return self.host.email + " " + self.group_name
    
    
class HostApplication(models.Model):
    host = models.ForeignKey(User,unique=False, on_delete=models.CASCADE)
    group_name = models.CharField(verbose_name='모임 이름',max_length=20, null=False, default='veterans')
    court_location = models.CharField(verbose_name='장소',max_length=100, null=False)
    intro = models.CharField(verbose_name='한줄 소개', max_length=200, null=False)

    def __str__(self):
        return self.host.email + " " + self.group_name + " " + self.intro
    
