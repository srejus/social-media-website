from django.urls import path
from . import views

urlpatterns=[
    path('follow_topic/<int:id>',views.follow_topic,name='follow_topic'),
    path('unfollow_topic/<int:id>',views.unfollow_topic,name='unfollow_topic'),
    path('topic/<int:id>',views.topic,name='topic'),
]