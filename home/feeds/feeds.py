from  home.models import Following, Post
from datetime import datetime, timedelta


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