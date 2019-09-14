from django.contrib import admin
from .models import Music, Genre, MusicFile


admin.site.register(Music)
admin.site.register(Genre)
admin.site.register(MusicFile)