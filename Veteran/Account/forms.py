from django import forms
from .models import Host

class HostForm(forms.ModelForm):
    
    class Meta:
        model = Host
        fields = ['host', 'group_name', 'court_location', 'intro']
        