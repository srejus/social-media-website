from django.http.response import HttpResponse
from django.shortcuts import render

from topics.models import Topic_follow

# Create your views here.
def follow_topic(request,id):
    usr = request,user
    if Topic_follow.objects.get(user_id = usr).exists():
        print("Exists....")
    else:
        print("Does not exists...")
    
    return HttpResponse("Ok")