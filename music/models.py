from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class Music(models.Model):
    genre = models.ForeignKey('music.Genre', on_delete=models.CASCADE, related_name='music')
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='music_owner')
    contributor = models.ManyToManyField('accounts.User', related_name='music_contributor')
    title = models.CharField(max_length=30)
    album_jacket = models.ImageField(blank=True, upload_to='img')
    seed_file = models.FileField(upload_to='audiofile')
    create_date = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)
    participants = models.IntegerField(default=0)
    MUSIC_COMPLETED, MUSIC_NOT_COMPLETED = 0, 1
    MUSIC_OPTION = (
        (MUSIC_COMPLETED, '완성'),
        (MUSIC_NOT_COMPLETED, '미완성')
    )
    music_option = models.SmallIntegerField(choices=MUSIC_OPTION)

    def __str__(self):
        return self.title


class MusicFile(models.Model):
    music = models.ForeignKey('music.Music', on_delete=models.CASCADE, related_name='music_file')
    file_name = models.CharField(max_length=20)
    music_file = models.FileField()

    def __str__(self):
        return self.file_name
