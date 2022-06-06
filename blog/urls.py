# we have made this url by your own
from django.urls import path
from . import views

urlpatterns = [
    # API for posting a comment
    path('postcomment', views.postComment, name='postComment'),


    path('',views.blogHome,name='blogHome'),
    path('<str:slug>',views.blogPost,name='blogPost'),
]
