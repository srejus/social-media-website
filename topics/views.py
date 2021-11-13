from django.http.response import HttpResponse
from django.shortcuts import render

from topics.models import Topic, Topic_follow

# Create your views here.
def follow_topic(request,id):
    usr = request.user
    topic = Topic_follow.objects.get(topic_id = id)
    if usr in topic.user_id:
        print("Exists....")
    else:
        print("Does not exists...")
    
    return HttpResponse("Ok")

def topic(request,id):
    tpc =Topic.objects.get(id = id)
    return render(request,'topic_info.html')