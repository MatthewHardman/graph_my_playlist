# Generated by Django 4.1.3 on 2022-12-05 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spotifyuserplaylist',
            name='user',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
