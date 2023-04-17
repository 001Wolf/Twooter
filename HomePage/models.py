from contextlib import nullcontext
from email.policy import default
from enum import unique
import uuid
from django.db import models

# Create your models here.
class BasicUserDB(models.Model):
    userID = models.UUIDField(null=False,
    editable=False)

    username = models.CharField(max_length=20,
    null=False)

    userTag = models.CharField(max_length=4,
    null=False)

class TweetDB(models.Model):
    user = models.ForeignKey(BasicUserDB, on_delete=models.CASCADE)
    
    tweetID = models.UUIDField(default=uuid.uuid4,
    unique=True,
    editable=False)

    message = models.CharField(max_length=300,
    null=False)

    created_on = models.BigIntegerField(null=False,
    editable=False,
    default=0)