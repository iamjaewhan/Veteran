from django import forms
from django.contrib.auth.hashers import check_password

from .models import User, UserManager
                

class UserCreationForm(forms.ModelForm):
    # 사용자 생성 폼
    email = forms.EmailField(
        label = ('Email'),
        required = True,
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control',
                'placeholder': ('Email address'),
                'required': 'True',
            }
        )
    )
    nickname = forms.CharField(
        label = ('Nickname'),
        required = True,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': ('Nickname'),
                'required': 'True',
            }
        )
    )
    
    phone = forms.CharField(
        label = ('phone'),
        required = True,
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
                'placeholder' : ('phone'),
                'required' : 'True',
            }
        )
    )
    
    password1 = forms.CharField(
        label = ('Password'),
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'placeholder': ('Password'),
                'required': 'True',
            }
        )
    )
    password2 = forms.CharField(
        label = ('Password confirmation'),
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'placeholder': ('Password confirmation'),
                'required': 'True',
            }
        )
    )

    class Meta:
        model = User
        fields = ('email', 'nickname')

    def clean_password2(self):
        # 두 비밀번호 입력 일치 확인
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.email = UserManager.normalize_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class HostForm(forms.Form):
    group_name = forms.CharField(
         label = (),
         widget = forms.TextInput(
             attrs = {
                 'class' : 'form-control',
                 'placeholder' : ('모임명'),
                 'required' : 'True',
             }
         )
     )
    
    intro = forms.CharField(
         label = (),
         widget = forms.TextInput(
             attrs = {
                 'class' : 'form-control',
                 'placeholder' : ('한 줄 소개'),
                 'required' : 'True',
             }
         )
     )
    
    court_location = forms.CharField(
         label = (),
         widget = forms.TextInput(
             attrs = {
                 'class' : 'form-control',
                 'placeholder' : ('경기 장소 주소'),
                 'required' : 'True',
             }
         )
     )
    
    court_detail_location = forms.CharField(
        label = (),
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
                'placeholder' : ('경기장 상세 주소'),
                'required' : 'False',
            }
        )
    )