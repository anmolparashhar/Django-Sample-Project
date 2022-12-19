from django.contrib import admin
from django.urls import path
from msadmin import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.Adminpage, name='index'),
    path('login',views.Adminlogin, name = 'login'),
    path('logout', views.Logoutpage, name = 'logout'),
    path('item', views.Create_item, name = 'item'),
    path('itemshow', views.Item_show, name= 'itemshow'),
    path('mix', views.Item_editdelete, name='mix'),
]
