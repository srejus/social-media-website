from  home.models import Following, Post
from datetime import datetime, timedelta
from topics.models import *


def feedalgo(id):
    #Fetch the Users followings
    followings=Following.objects.filter(Bywho=id)

    
    flst=[]
    for i in followings:
        try:
            flst.append(i.whom.id)
        except:
            pass

    time_threshold = datetime.now() - timedelta(hours=3)

    print(time_threshold)

    qs=Post.objects.filter(UID__in=flst).filter(Time__lt=time_threshold).order_by('-Time')
    print(qs)

#Use nested for loops for out the data


    return(qs)


def suggestalgo(id):
    #Fetch the Users followings
    followings=Following.objects.filter(Bywho=id)

    
    flst=[]
    for i in followings:
        try:
            flst.append(i.whom.id)
        except:
            pass

    time_threshold = datetime.now() - timedelta(hours=3)

    print(time_threshold)

    qs=Post.objects.exclude(UID__in = flst).filter(Time__lt=time_threshold).order_by('-Time')
   

#Use nested for loops for out the data


    return(qs)

def topic_algo(id):

   #Fetch the Users followings
    followings=Following.objects.filter(Bywho=id)

    
    flst=[]
    for i in followings:
        try:
            flst.append(i.whom.id)
        except:
            pass

    #Users topics

    tps = Topic_follow.objects.filter(user_id = id)

    tpc_lst = []

    for i in tps:
        tpc_lst.append(i.topic_id)
    
    qs=Post.objects.exclude(UID__in = flst).filter(post_topic__in = tpc_lst)
    print(qs)

    return(qs)