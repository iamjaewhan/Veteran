from rest_framework import serializers

from accounts.serializers import HostSerializer
from .models import Game

class GameSerializer(serializers.ModelSerializer):
    host = HostSerializer(read_only = True)
    
    class Meta:
        model = Game
        fields = '__all__'