from datetime import datetime
import re
import uuid

from django.shortcuts import HttpResponse, redirect, render
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpRequest

from Twooter.session_authentication import SA

from .forms import LoginForm
from .models import LoginDetails, SessionDetails

# Create your views here.
def index(request:HttpRequest):
    status = ''
    response = HttpResponse()
    if SA.validateForLogin(request):
        return redirect('/home')
    #if login attempt has been made
    if len(request.POST) > 0:
        #see if the username and passowrd is correct and shit
        user = None
        try:
            #Check if provided is a email or username
            if checkEmail(request.POST.get('username')):
                user = LoginDetails.objects.get(email_id=request.POST.get('username'), password=request.POST.get('password'))   
            else:
                user = LoginDetails.objects.get(username=request.POST.get('username'), password=request.POST.get('password'))
        except ObjectDoesNotExist:
            return render(request, 'LoginPage/index.html', {'form':LoginForm, 'errStatus': "Invalid Username or Password"})
        except MultipleObjectsReturned:
            user = LoginDetails.objects.filter(email_id=request.POST.get('username'), password=request.POST.get('password'))[0]
        #if yes then continue adding session
        sessionID = uuid.uuid4()
        new_session = SessionDetails(sessionID=sessionID, user=user, created_on=datetime.now().timestamp())
        new_session.save()
        #adding entry
        response = redirect('/home')
        #adding cookies
        response.set_cookie('sessionID' , sessionID)
        response.set_cookie('userID' , user.userID)

        #redirecting to home page
        return response


    response = render(request, 'LoginPage/index.html', {'form':LoginForm, 'errStatus': status})

    return response



def checkEmail(s):
    pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pat,s):
        return True
    return False