from email.policy import default
import uuid
from django.db import models

# Create your models here.
class RegisterSessionDetails(models.Model):

    regSessionID = models.UUIDField(default=uuid.uuid4,
    editable=False)

    created_on = models.BigIntegerField(null=False,
    editable=False)

    regUserID = models.UUIDField(default=uuid.uuid4, 
    editable=False,
    unique=True)

    email = models.EmailField(null=False)

    username = models.CharField(max_length=20,null=False)
    
    password = models.CharField(max_length=20,null=False)

    authCode = models.CharField(max_length=5,null=False)