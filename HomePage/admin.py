from django.contrib import admin
from .models import BasicUserDB, TweetDB
# Register your models here.
admin.site.register(BasicUserDB)
admin.site.register(TweetDB)