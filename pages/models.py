from django.db import models

# Create your models here.
class SpotifyUserPlaylist(models.Model):
    user = models.CharField(max_length = 150, unique=True)
    access_token = models.CharField(max_length=150)
    playlist = models.JSONField()

    