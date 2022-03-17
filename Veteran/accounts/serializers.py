from .models import User, HostApplication
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','nickname','phone','password']
        
class HostAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostApplication
        fields = '__all__'