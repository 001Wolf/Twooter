from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('logOut/', views.logOut, name='logOut'),
    path('getTweets', views.getTweets, name='getTweets'),
    path('sendTweet', views.sendTweet, name='sendTweet')
]