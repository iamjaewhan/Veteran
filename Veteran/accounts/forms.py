from django import forms
from django.contrib.auth.hashers import check_password

from .models import User, UserManager

class UserLoginForm(forms.Form):
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
    
    password = forms.CharField(
        label = ('Password'),
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'placeholder': ('Password'),
                'required': 'True',
            }
        )
    )
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        if email and password:
            try:
                user = User.objects.get(email=email)
                if not check_password(password, user.password):
                    self.add_error('password', "올바르지 않은 정보입니다.")
                else:
                    self.user_id = user.id
            except Exception:
                self.add_error('email', "올바르지 않은 정보입니다.ㄴ")
                

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