from django.db import models

# Create your models here.
class Playlist(models.Model):
    body = models.JSONField