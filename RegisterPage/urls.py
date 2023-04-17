from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('verify/', views.verify),
    path('regCheckUsername/<str:username>/', views.checkUsername, name="regCheckUsername"),
]