# Generated by Django 2.2 on 2021-06-04 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_album_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='file_type',
        ),
        migrations.AddField(
            model_name='song',
            name='audio_file',
            field=models.FileField(default='', upload_to=''),
        ),
    ]
