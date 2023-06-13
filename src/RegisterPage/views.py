from datetime import datetime
import random
import string
import uuid
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail

from HomePage.models import BasicUserDB
from LoginPage.models import LoginDetails
from RegisterPage.models import RegisterSessionDetails
from ProfilePage.models import UserProfile
from Twooter.settings import EMAIL_HOST_USER

from .forms import RegisterForm
from Twooter.session_authentication import SA

# Create your views here.
def index(request):

    response = HttpResponse()
    if SA.validateForLogin(request):
        return redirect('/home')

    if len(request.POST) > 0:

        response = redirect('verify/')
        
        # Sending Mail
        authCode = generateAuthCode()
        subject = "Your Verification Code"
        message = "Your Verification Code for Twooter Register is: " + authCode
        reciepent = request.POST['email']
        send_mail(subject, message, EMAIL_HOST_USER, [reciepent], fail_silently=False)

        #Creating Entries and Cookies
        regSessionID = uuid.uuid4()
        regUserID = uuid.uuid4()
        response.set_cookie('regSessionID', regSessionID)
        response.set_cookie('regUserID', regUserID)

        entry = RegisterSessionDetails(regSessionID=regSessionID,
        created_on=datetime.now().timestamp(),
        regUserID=regUserID,
        email=request.POST['email'],
        username=request.POST['username'],
        password=request.POST['password'],
        authCode=authCode)
        entry.save()

        return response
    
    return render(request, 'RegisterPage/index.html', {'form':RegisterForm()})

def verify(request):
    response = render(request, 'RegisterPage/verify.html', {'authStatus':''})
    response = SA.validateForRegister(request, response)
    if len(request.POST) > 0:
        if SA.validateForRegisterBool(request):
            user = RegisterSessionDetails.objects.filter(regSessionID=request.COOKIES['regSessionID'], regUserID=request.COOKIES['regUserID'])
            if len(user) > 0:
                if request.POST['code'] == user[0].authCode:

                    response = redirect('/login')

                    #Create new LoginDetails Entry
                    loginDetail = LoginDetails(username=user[0].username,
                    password=user[0].password,
                    email_id=user[0].email,
                    userID=user[0].regUserID)

                    loginDetail.save()

                    #Create new BasicUserDB Entry
                    basicUser = BasicUserDB(userID=user[0].regUserID,
                    username=user[0].username,
                    userTag=random.randint(1000,9999))
                    
                    basicUser.save()

                    #Create new UserProfile Entry
                    profileUser = UserProfile(user=basicUser)

                    profileUser.save()

                    #Delete RegSession Entry
                    user.delete()

                    #Delete Cookies
                    response.delete_cookie('regSessionID')
                    response.delete_cookie('regUserID')
                    
                    #Redirect to Login Page
                    return response
                else:
                    response = render(request, 'RegisterPage/verify.html', {'authStatus':'Wrong Authentication Code'})
            else:
                response = redirect('/login')
        else: 
            response = redirect('/login')
    return response

def checkUsername(request, username):
    # username = "001Wolf"
    if len(LoginDetails.objects.filter(username=username)) > 0:
        return JsonResponse({"exist":True})
    return JsonResponse({"exist":False})

def generateAuthCode():
    return ''.join(random.choices(string.ascii_letters, k=5))