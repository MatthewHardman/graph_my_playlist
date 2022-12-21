from django.db import models

# Create your models here.
class SpotifyToken(models.Model):
    user = models.JSONField(unique=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    token_type = models.CharField(max_length=50)
