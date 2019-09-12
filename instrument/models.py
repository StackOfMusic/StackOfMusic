from django.db import models


class Instrument(models.Model):
    name = models.CharField(max_length=20)
    music = models.ManyToManyField('music.Music', related_name='instrument')

    def __str__(self):
        return self.name