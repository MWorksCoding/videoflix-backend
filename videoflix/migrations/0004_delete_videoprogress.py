# Generated by Django 5.1.1 on 2024-10-23 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videoflix', '0003_alter_video_genre_videoprogress'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VideoProgress',
        ),
    ]