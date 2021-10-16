from  home.models import Following, Post

def feedalgo(id):
    #Fetch the Users followings
    followings=Following.objects.filter(Bywho=id)

    
    flst=[]
    for i in followings:
        try:
            flst.append(i.whom.id)
        except:
            pass


    qs=Post.objects.filter(UID__in=flst).order_by('-Time')
    print(qs)

#Use nested for loops for out the data


    return(qs)