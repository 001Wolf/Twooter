from datetime import datetime
from email.policy import default
import uuid
from django.db import models

# Create your models here.
class LoginDetails(models.Model):

    username = models.CharField(primary_key=True,
    max_length=20,
    null=False)

    password = models.CharField(max_length=20,
    null=False)

    email_id = models.EmailField()

    userID = models.UUIDField(default=uuid.uuid4, 
    editable=False,
    unique=True)

class SessionDetails(models.Model):

    sessionID = models.UUIDField(default=uuid.uuid4,
    editable=False)

    created_on = models.BigIntegerField(null=False,
    editable=False)

    user = models.ForeignKey(LoginDetails, on_delete=models.CASCADE)