from.import views
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('', views.home, name='home'),
    path('home/contact/', views.contact, name='contact'),
    path('about/', views.about, name='about') , 
    path('search/', views.search, name='search'),
    path('signup', views.signup, name='signup'),
    path('login', views.handlelogin, name='handlelogin'),
    path('logout', views.handlelogout, name='handlelogout'),
]