from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from home.models import Post

from topics.models import Topic, Topic_follow

# Create your views here.
def follow_topic(request,id):
    
    tpc =Topic.objects.get(id = id)
    try:
        x=Topic_follow(user_id = request.user , topic_id = tpc)
        x.save()
    except:
       pass
    return redirect('/topic/'+str(id))

def unfollow_topic(request,id):
    
    tpc =Topic.objects.get(id = id)
    if Topic_follow.objects.filter(user_id = request.user , topic_id = tpc).exists():
        x=Topic_follow.objects.get(user_id = request.user , topic_id = tpc)
        x.delete()

    return redirect('/topic/'+str(id))
 
 #Code works when click on view button
def topic(request,id):
    tpc =Topic.objects.get(id = id)

    flw = False

    #Fetched the posts that related to the topic tag

    pst = Post.objects.filter(post_topic = tpc.topic_name)

    #Count total number of followers for this particular topic

    count = Topic_follow.objects.filter(topic_id = tpc).count()


    
    #Check whether the user follow this topic or not
    if Topic_follow.objects.filter(user_id = request.user , topic_id = tpc).exists():
        flw = True
    else:
        flw = False
    return render(request,'topic_info.html',{'tp':tpc,'fw':flw,'c':count,'post':pst})