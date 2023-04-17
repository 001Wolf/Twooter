from django.db import models
from HomePage.models import BasicUserDB

# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(BasicUserDB, 
    on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True,
    null=False)

    profile_pic = models.ImageField(upload_to='profile_pics/')

    bio = models.TextField()