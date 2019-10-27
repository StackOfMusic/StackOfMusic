from django.contrib import admin
from .models import Music, Genre, SubMusic


admin.site.register(Music)
admin.site.register(Genre)
admin.site.register(SubMusic)