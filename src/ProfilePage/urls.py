from django.urls import path


from . import views

urlpatterns = [
    path('', views.index),
    path('<int:tweet_id>/', views.tweetInfo),
    path('edit/', views.edit),
    path('update/', views.update),
    path('ownsAccount/', views.ownsAccount, name='ownsAccount')
]