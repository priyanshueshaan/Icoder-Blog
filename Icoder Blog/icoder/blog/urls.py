from.import views
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('/postcomment', views.PostComment, name='PostComment'), 
    path('/', views.bloghome, name='bloghome'),
    path('<str:slug>',views.blogpost,name='blogpost'),
]