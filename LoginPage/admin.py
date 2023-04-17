from django.contrib import admin
from .models import LoginDetails, SessionDetails 

# Register your models here.
admin.site.register(LoginDetails)
admin.site.register(SessionDetails)