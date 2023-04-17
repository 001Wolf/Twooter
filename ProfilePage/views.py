from datetime import datetime
import os
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect, render
from django.core.exceptions import ObjectDoesNotExist
from HomePage.models import TweetDB
from HomePage.models import BasicUserDB
from ProfilePage.forms import EditProfile

from Twooter.session_authentication import SA

from .models import UserProfile

# Create your views here.
def index(request, account_name):
    response = HttpResponse()
    response = SA.validate(request, response)
    if SA.validateForLogin(request):
        try:
            user = UserProfile.objects.get(user__username=account_name)
            tweets_list = TweetDB.objects.filter(user__username=account_name)
            tweets = {}
            for twt in tweets_list:
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
                tweets[int(twt.tweetID)] = {'tweet': twt, 'created_on' : created_on}
            logUser = UserProfile.objects.filter(user__userID=request.COOKIES["userID"])[0]
            response = render(request,'ProfilePage/profile.html', {'logUser':logUser,'user':user, 'tweets':tweets})
        except ObjectDoesNotExist:
            response = HttpResponse("Account like that does not exist")
    return response

def tweetInfo(request, account_name, tweet_id):
    response = HttpResponse()
    response = SA.validate(request, response)
    if SA.validateForLogin(request):
        try:
            tweet = TweetDB.objects.get(user__username=account_name, tweetID=tweet_id)
            profile_pic = UserProfile.objects.filter(user=tweet.user)[0].profile_pic
            user = UserProfile.objects.filter(user__userID=request.COOKIES["userID"])[0]
            response = render(request, 'ProfilePage/tweet.html', {'tweet':tweet, 'created_on':datetime.fromtimestamp(tweet.created_on),'profile_pic':profile_pic, 'user':user})
        except ObjectDoesNotExist:
            response = HttpResponse("Page like was not found")
    return response

def edit(request, account_name):
    response = HttpResponse()
    response = SA.validate(request, response)
    if SA.validateForLogin(request):
        user = BasicUserDB.objects.filter(username=account_name, userID=request.COOKIES['userID'])
        if len(user) > 0:
            user = UserProfile.objects.filter(user=user[0])
            if len(user) > 0:
                response = render(request, 'ProfilePage/profileEdit.html', {'user': user[0]})
            else: 
                response = redirect('/login/')
        else:
            user = BasicUserDB.objects.filter(userID=request.COOKIES['userID'])
            if len(user) > 0:
                response = redirect('/' + user[0].username + '/edit')
            else:
                response = redirect('/login/')
    return response

def update(request, account_name):
    response = HttpResponse()
    response = SA.validate(request, response)
    if SA.validateForLogin(request):
        if request.method == 'POST':
            print(request.POST)
            print(type(request.FILES.get('profile_pic')))
            new_profile = UserProfile.objects.filter(user=BasicUserDB.objects.filter(userID=request.COOKIES['userID'])[0])[0]
            old_profile_pic = ''
            if request.POST.get('bio') != "":
                new_profile.bio = request.POST.get('bio')
            if request.FILES.get('profile_pic') != None:
                file = request.FILES.get('profile_pic')
                old_profile_pic = new_profile.profile_pic
                file.name = str(int(new_profile.user.userID)) + file.name[file.name.index('.'):]
                new_profile.profile_pic = file
            new_profile.save()
            # if old_profile_pic != "":
            #     deleteOldPic(old_profile_pic,new_profile.profile_pic)
            response = redirect('/' + account_name + "/")
        else:
            response = redirect('/' + account_name + "/")
    return response

def ownsAccount(request, account_name):
    if SA.validateForLogin(request):
        user = BasicUserDB.objects.filter(username=account_name, userID=request.COOKIES['userID'])
        if len(user) > 0:
            return JsonResponse({'ownsAccount': True})
        else:
            return JsonResponse({'ownsAccount': False})
    else:
        return JsonResponse({'logOutLMAO': True})

def deleteOldPic(oldFile, newFile):
    try:
        os.remove(str(oldFile.file))
        os.rename(str(newFile.file), str(oldFile.file))
    except FileNotFoundError:
        pass
    except FileExistsError:
        pass