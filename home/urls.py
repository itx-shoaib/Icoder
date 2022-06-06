# we have made this url by your own
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('search/',views.search,name='search'),
    path('signup',views.handleSignUp,name='signup'),
    path('login',views.handleLogin,name='handlelogin'),
    path('logout',views.handleLogout,name='handlelogout'),
]
