from django.db import models
from datetime import date
import datetime
from authemail.models import EmailUserManager, EmailAbstractUser

class MyUser(EmailAbstractUser):
	objects = EmailUserManager()
 
class Video(models.Model):
    
    GENRES = [
    ("fitness", "Fitness"),
    ("chess", "Chess"),
    ("pets", "Pets"),
    ("holiday", "Holiday"),
    ]
        
    created_at = models.DateField(default=datetime.date.today)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to="videos", blank=True, null=True)
    thumbnail_file = models.FileField(upload_to="thumbnails", blank=True, null=True)
    genre = models.CharField(max_length=20, choices=GENRES, default="fitness")
