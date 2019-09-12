from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class Music(models.Model):
    genre = models.ForeignKey('music.Genre', on_delete=models.CASCADE, related_name='genre')
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='music_owner')
    contributor = models.ManyToManyField('accounts.User', related_name='music_contributor')
    title = models.CharField(max_length=30)
    create_date = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)
    participants = models.IntegerField(default=0)

    def __str__(self):
        return self.title
