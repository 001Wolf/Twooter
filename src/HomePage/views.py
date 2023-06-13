
from datetime import datetime
import uuid
from django.shortcuts import HttpResponse, redirect, render
from django.template import loader
from django.http import HttpRequest, JsonResponse
from LoginPage.models import LoginDetails
from HomePage.models import BasicUserDB
from LoginPage.models import SessionDetails
from HomePage.models import TweetDB
from ProfilePage.models import UserProfile

from Twooter.session_authentication import SA

# Create your views here.
def index(request:HttpRequest):
    response:HttpResponse = HttpResponse()

    #Authenticating Session
    response = SA.validate(request=request, response=response)

    if(SA.validateForLogin(request)):
        user = BasicUserDB.objects.filter(userID=request.COOKIES['userID'])
        profile_pic = UserProfile.objects.filter(user=user[0])[0].profile_pic
        response = render(request, 'HomePage/index.html', {'user':user[0], 'profile_pic':profile_pic})

    return response

def logOut(request):
    session = SessionDetails.objects.filter(sessionID=request.COOKIES['sessionID'], user__userID=request.COOKIES['userID'])
    if len(session) > 0:
        session[0].delete()
        return JsonResponse({'loggedOut':True})
    return JsonResponse({'loggedOut':False})

def getTweets(request):
    tweets = TweetDB.objects.all()
    tweets_dict = {}
    for twt in tweets:
        created_on = datetime.now().timestamp() - twt.created_on
        # If greater than 60 seconds
        if created_on >= 60:
            created_on /= 60
            # If greater than 60 minutes
            if created_on >= 60:
                created_on /= 60
                # If greater than 24 hours
                if created_on >= 24:
                    created_on /= 24
                    # If greater than 30 days
                    if created_on >= 30:
                        created_on /= 30
                        # If greater than 12 months
                        if created_on >= 12:
                            created_on /= 12
                            created_on = str(int(created_on)) + 'year'
                        else:
                            created_on = str(int(created_on)) + 'months'
                    else:
                        created_on = str(int(created_on)) + 'days'
                else:
                    created_on = str(int(created_on)) + 'hr'
            else:
                created_on = str(int(created_on)) + 'm'
        else:
            created_on = str(int(created_on)) + 's'
        profile_pic = str(UserProfile.objects.filter(user=twt.user)[0].profile_pic)
        
        tweets_dict[int(twt.tweetID)] = {'author':twt.user.username, 'message':twt.message, 'created_on':created_on, 'profile_pic': profile_pic}
    return JsonResponse({'tweets':tweets_dict})

def sendTweet(request):
    if not SA.validateForLogin(request):
        return JsonResponse({'logOutLMAO':True})
    else:
        tweet = TweetDB(user=BasicUserDB.objects.filter(userID=request.COOKIES['userID'])[0],
        message=request.POST['message'],
        created_on=datetime.now().timestamp())
        tweet.save()
        return JsonResponse({'tweetSent':True})