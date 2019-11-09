from django.db import models
from django.urls import reverse
from accounts.models import User


class Genre(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class Music(models.Model):
    genre = models.ForeignKey('music.Genre', on_delete=models.CASCADE, related_name='music')
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='music_owner')
    # contributor = models.ManyToManyField('accounts.User', related_name='music_contributor')
    title = models.CharField(max_length=30)
    album_jacket = models.ImageField(blank=True, upload_to='img')
    seed_file = models.FileField(upload_to='audiofile')
    instrument = models.ForeignKey('instrument.Instrument', on_delete=models.CASCADE, related_name='music')
    create_date = models.DateTimeField(auto_now_add=True)
    participants = models.IntegerField(default=0)
    MUSIC_COMPLETED, MUSIC_NOT_COMPLETED = 0, 1
    MUSIC_OPTION = (
        (MUSIC_COMPLETED, '완성'),
        (MUSIC_NOT_COMPLETED, '미완성')
    )
    music_option = models.SmallIntegerField(choices=MUSIC_OPTION)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('create_music:working_music_detail', args=(self.pk,))

    # def is_owner(self):
    #     return self.owner == User.USER_TEACHER

    def is_complete(self):
        return self.music_option == Music.MUSIC_COMPLETED

    def is_not_complete(self):
        return self.music_option == Music.MUSIC_NOT_COMPLETED


class SubMusic(models.Model):
    music = models.ForeignKey('music.Music', on_delete=models.CASCADE, related_name='sub_musics')
    contributor = models.ForeignKey('accounts.User', related_name='sub_music', on_delete=models.CASCADE)
    instrument = models.ForeignKey('instrument.Instrument', on_delete=models.CASCADE, related_name='sub_music')
    music_file = models.FileField(upload_to='audiofile')
    create_date = models.DateTimeField(auto_now_add=True)
    ACCEPT, PENDING = 0, 1
    STATUS = (
        (ACCEPT, '머지'),
        (PENDING, '대기'),
    )
    status = models.SmallIntegerField(choices=STATUS)


# Music.objects.prefetch_related('sub_musics').filter(instrument_id__in=[], sub_musics__instrument_id__in=[])
# class CompletedMusic(models.Model):
