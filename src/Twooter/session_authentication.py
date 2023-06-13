#Function
from datetime import datetime
import uuid

from django.shortcuts import HttpResponse, redirect
from LoginPage.models import SessionDetails
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.core.exceptions import ObjectDoesNotExist

from LoginPage.models import LoginDetails
from RegisterPage.models import RegisterSessionDetails

class SA:
    
    def validate(request:HttpRequest, response:HttpResponse):

        #Getting cookies
        sessionID = request.COOKIES.get('sessionID')
        userID = request.COOKIES.get('userID')

        #if cookies does not exist, send them back to login page
        if sessionID == None and userID == None:
            response = redirect('/login')
            #print statement for debugging
            print('Cookies does not exist')
            return response

        #creating local scope user
        user = None
        #if session values are incorrect, this can only happen is someone is trying to session hijack but is only half good LOL
        try:
            #creating user manually for testing
            # user = SessionDetails.objects.get(sessionID="96870bb2-ce8b-434d-be68-fed84f03a802",user__userID="c6149e7b-9904-40d2-a07e-bf75d797c935")
            #getting user
            user = SessionDetails.objects.get(sessionID=sessionID,user__userID=userID)
        except ObjectDoesNotExist:
            #if session does not exist, send them back to login
            response = redirect('/login')
            #print statement for debugging
            print('BITCH HACKER or that sessionID is whack')
            return response
        except Exception as ex:
            print(ex)
        

        #If session invalid, delete cookies and entry from db, and send them back to login page
        if SA.session_expired(sessionTime=user.created_on):
            #go to login
            response = redirect('/login')
            #Deleting cookies
            response.delete_cookie('sessionID')
            response.delete_cookie('userID')
            #Deleting entry
            user.delete()
            #print statement for debugging
            print('EXPIRED!')
            return response

        #If session is valid, return to current page BABY!
        else:
            return response

    def validateForLogin(request:HttpRequest):

        #Getting cookies
        sessionID = request.COOKIES.get('sessionID')
        userID = request.COOKIES.get('userID')

        #if cookies does not exist, send them back to login page
        if request.COOKIES.get('sessionID') == None and request.COOKIES.get('userID') == None:
            return False

        #creating local scope user
        user = None
        #if session values are incorrect, this can only happen is someone is trying to session hijack but is only half good LOL
        try:
            user = SessionDetails.objects.get(sessionID=sessionID,user__userID=userID)
        except ObjectDoesNotExist:
            return False
        except Exception as ex:
            print(ex)
            return False
        

        #If session invalid, delete cookies and entry from db, and send them back to login page
        if SA.session_expired(sessionTime=user.created_on):
            #Deleting entry
            user.delete()
            return False

        #If session is valid, return to home page BABY!
        else:
            return True

    def validateForRegister(request:HttpRequest, response:HttpResponse):

        #Getting cookies
        sessionID = request.COOKIES.get('regSessionID')
        userID = request.COOKIES.get('regUserID')

        #if cookies does not exist, send them back to login page
        if sessionID == None and userID == None:
            response = redirect('/login')
            #print statement for debugging
            return response

        #If Cookies exist, check if it is still valid
        #creating local scope user
        user = None
        #if session values are incorrect, this can only happen is someone is trying to session hijack but is only half good LOL
        try:
            #creating user manually for testing
            # user = SessionDetails.objects.get(sessionID="96870bb2-ce8b-434d-be68-fed84f03a802",user__userID="c6149e7b-9904-40d2-a07e-bf75d797c935")
            #getting user
            user = RegisterSessionDetails.objects.get(regSessionID=sessionID,regUserID=userID)
        except ObjectDoesNotExist:
            #if session does not exist, send them back to login
            response = redirect('/login')
            #print statement for debugging
            return response
        except Exception as ex:
            print(ex)
        #If cookies isnt valid, delete cookies and entry
        if SA.session_expired_reg(sessionTime=user.created_on):
            #go to login
            response = redirect('/login')
            #Deleting cookies
            response.delete_cookie('regSessionID')
            response.delete_cookie('regUserID')
            #Deleting entry
            user.delete()
            #print statement for debugging
            return response
        #If valid leave them be
        return response

    def validateForRegisterBool(request:HttpRequest):

        #Getting cookies
        sessionID = request.COOKIES.get('regSessionID')
        userID = request.COOKIES.get('regUserID')

        #if cookies does not exist, send them back to login page
        if sessionID == None and userID == None:
            return False

        #If Cookies exist, check if it is still valid
        #creating local scope user
        user = None
        #if session values are incorrect, this can only happen is someone is trying to session hijack but is only half good LOL
        try:
            #creating user manually for testing
            # user = SessionDetails.objects.get(sessionID="96870bb2-ce8b-434d-be68-fed84f03a802",user__userID="c6149e7b-9904-40d2-a07e-bf75d797c935")
            #getting user
            user = RegisterSessionDetails.objects.get(regSessionID=sessionID,regUserID=userID)
        except ObjectDoesNotExist:
            return False
        except Exception as ex:
            print(ex)
            return False
        #If cookies isnt valid, delete cookies and entry
        if SA.session_expired_reg(sessionTime=user.created_on):
            user.delete()
            #print statement for debugging
            return False
        #If valid leave them be
        return True     

    def session_expired(sessionTime:int):
        #answer
        ans = False
        #in seconds
        expiry_time = 600 #10 minutes for testing, most probably will be in days
        if (datetime.now().timestamp() - sessionTime) > expiry_time:
            ans = True
        return ans

    def session_expired_reg(sessionTime:int):
        #answer
        ans = False
        #in seconds
        expiry_time = 60 #20 seconds for testing, most probably will be in days
        if (datetime.now().timestamp() - sessionTime) > expiry_time:
            ans = True
        return ans