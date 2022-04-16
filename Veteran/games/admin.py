from django.contrib import admin
from .models import Game, Game_Participant, HostGame

# Register your models here.
admin.site.register(Game)
admin.site.register(Game_Participant)
admin.site.register(HostGame)