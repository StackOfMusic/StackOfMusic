from django.core.files.storage import FileSystemStorage
from django.db import models
from django.urls import reverse

from StackOfMusic import settings
from accounts.models import User


# class CustomFileField(models.FileField):
#     attr_class = FieldFile
#     interval = 0
#
#     def pre_save(self, model_instance, add):
#         file = super().pre_save(model_instance, add)
#         if file and not file._committed:
#             file.save(file.name, file.file, save=False)
#         return file
#
#     def set_interval(self, interval):
#         self.interval = interval


private_storage = FileSystemStorage(location=settings.STATIC_URL + settings.STATICFILES_LOCATION + '/')


class Genre(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class Music(models.Model):
    genre = models.ForeignKey('music.Genre', on_delete=models.CASCADE, related_name='music')
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='music_owner')
    title = models.CharField(max_length=30)
    album_jacket = models.ImageField(blank=True, upload_to='img')
    seed_file = models.FileField(upload_to='audiofile')
    completed_music = models.FileField(upload_to='audiofile', blank=True, null=True)
    instrument = models.ForeignKey('instrument.Instrument', on_delete=models.CASCADE, related_name='music', blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    liked_music = models.ManyToManyField('accounts.User', blank=True, related_name='music')
    participants = models.IntegerField(default=0)
    MUSIC_COMPLETED, MUSIC_NOT_COMPLETED = 0, 1
    MUSIC_OPTION = (
        (MUSIC_COMPLETED, '완성'),
        (MUSIC_NOT_COMPLETED, '미완성')
    )
    music_option = models.SmallIntegerField(choices=MUSIC_OPTION)
    BEFORE_UPDATE, UPDATING, AFTER_UPDATE = 0, 1, 2
    UPDATE_STATUS = (
        (BEFORE_UPDATE, '업데이트 전'),
        (UPDATING, '업데이트 중'),
        (AFTER_UPDATE, '업데이트 후'),
    )
    update_status = models.SmallIntegerField(choices=UPDATE_STATUS)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('create_music:working_music_detail', args=(self.pk,))

    @property
    def total_likes_user(self):
        return self.liked_music.count()

    def is_complete(self):
        return self.music_option == Music.MUSIC_COMPLETED

    def is_not_complete(self):
        return self.music_option == Music.MUSIC_NOT_COMPLETED


class SubMusic(models.Model):
    music = models.ForeignKey('music.Music', on_delete=models.CASCADE, related_name='sub_musics')
    contributor = models.ForeignKey('accounts.User', related_name='sub_music', on_delete=models.CASCADE)
    instrument = models.ForeignKey('instrument.Instrument', on_delete=models.CASCADE, related_name='sub_music')
    music_file = models.FileField(upload_to='audiofile')
    convert_music_file = models.FileField(upload_to=private_storage)
    create_date = models.DateTimeField(auto_now_add=True)
    ACCEPT, PENDING = 0, 1
    STATUS = (
        (ACCEPT, '머지'),
        (PENDING, '대기'),
    )
    status = models.SmallIntegerField(choices=STATUS)
    BEFORE_UPDATE, UPDATING, AFTER_UPDATE = 0, 1, 2
    UPDATE_STATUS = (
        (BEFORE_UPDATE, '업데이트 전'),
        (UPDATING, '업데이트 중'),
        (AFTER_UPDATE, '업데이트 후'),
    )
    update_status = models.SmallIntegerField(choices=UPDATE_STATUS)


class Comment(models.Model):
    music = models.ForeignKey('music.Music', on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='comment')
    comment_text = models.TextField()

    def __str__(self):
        return self.comment_text
# Music.objects.prefetch_related('sub_musics').filter(instrument_id__in=[], sub_musics__instrument_id__in=[])
# class CompletedMusic(models.Model):
