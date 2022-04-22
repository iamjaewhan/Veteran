from django.contrib import admin
from .models import Game, GameParticipant, HostGame

# Register your models here.
admin.site.register(Game)
admin.site.register(GameParticipant)
admin.site.register(HostGame)