from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import logout
from . feeds import feeds
from . models import *
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login



import smtplib

from django.db.models import Q 


def send_mail(to,msg):
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login('memail@gmail.com', '************')
            server.sendmail('memail@gmail.com', to, msg)
            return 0


# def mail(request):
#             message = 'Subject: {}\n\n{}'.format('SUBJECT',' Hello  this is a mail')
#             send_mail('to@gmail.com',message)
#             return JsonResponse({'res':'wee'})
# Create your views here.

@login_required(login_url='login')
def index(request):
    id=request.user.id
    if Following.objects.filter(Bywho=id).exists():
        myfeeds=feeds.feedalgo(id)
        suggest_feeds=feeds.suggestalgo(id)
        return render(request,'index.html',{'myfeed':myfeeds,'sf':suggest_feeds})
    else:
        x=Account.objects.order_by('?')[:11]
        return render(request,'index.html',{'y':x})

def Login(request):
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("pass1")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
  
        else:
            messages.warning(request,'Password or Username does not match!')
            return render(request,'login.html')
        return index(request)
    return render(request,'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        name=request.POST.get("name")
        password1 = request.POST.get("pass1")
        password2 = request.POST.get("pass2")

        if username == '':
            messages.warning(request, 'Enter Username')
            return render(request, 'signup.html')

        # Checking Password Strength(Length only)
        if len(password1) < 8:
            messages.warning(request, 'Password is too short!')
            return render(request, 'signup.html')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username already exists!')
                return render(request, 'signup.html')
            else:
                user = User.objects.create_user(
                username=username, password=password1)
                user.save()

                profile=Account(user=user,Name=name)
                profile.save()


                return Login(request)
        else:
            messages.warning(request, 'Password not matching!')
            return render(request, 'signup.html')
    return render(request, 'signup.html')

@login_required(login_url='login')
def profile(request,id):
    prof=Account.objects.get(user=id)
    followers=Following.objects.filter(whom=id).count()
    followings=Following.objects.filter(Bywho=id).count()
    #Fetch the post
    post=Post.objects.filter(UID=id)
    if Following.objects.filter(Bywho=request.user.id).filter(whom=id).exists():
        isFollow=True
    else:
        isFollow=False
    return render(request,'profile.html',{'p':prof,'i':isFollow,'folowr':followers,'folow':followings,'pst':post})

@login_required(login_url='login')
def follow(request,id):
    print(id)
    if Following.objects.filter(Bywho=request.user.id).filter(whom=id).exists():
        x=Following.objects.filter(Bywho=request.user.id).filter(whom=id)
        x.delete()
    else:
        usr=User.objects.get(id=id)
        if usr != request.user:
            x=Following(Bywho=request.user,whom=usr)
            x.save()

            #Fetch user email to send mail
            # try:
           
            #     email_ac=Account.objects.get(user=usr)
            #     message = 'Subject: {}\n\n{}'.format('New Follower!',' Hi user,'+email_ac.Name+' started following you')
            #     send_mail(email_ac.Email,message)
            # except:
            #     pass
        
    # return redirect('/profile/'+id)
    return profile(request,id=id)

def upload(request):
    if request.method == 'POST':
        capt=request.POST.get('caption')
        img=request.FILES.get('image')

        curent_ac=Account.objects.get(user=request.user)

        x=Post(UID=request.user,user=curent_ac,Caption=capt,Img=img)
        x.save()

        #Fetch Lst of followers to send mail
        # mail_lst=Following.objects.filter(whom=request.user)

        # for i in mail_lst:
        #     try:
               
        #         ac=Account.objects.get(user=i.Bywho)

                
        #         me=Account.objects.get(user=request.user).Name

        #         message = 'Subject: {}\n\n{}'.format(me+' posted an Update',' Hi user,'+ac.Name+' started following you')
        #         send_mail(ac.Email,message)
        #     except:
        #         pass


        return redirect('profile/'+str(request.user.id))
    return render(request,'upload.html')

@login_required(login_url='login')
def react(request):
    if request.method == 'POST':
        post_id=request.POST.get('pid')
    
        post=Post.objects.get(id=post_id)
        allLikes=post.Likes.all()
        print(allLikes)
        if len(allLikes) == 0:
            post.Likes.add(request.user)
            c=post.Likes.count()
            post.Total_likes=c
            post.save()
            like=1
        else:
            for t in allLikes:
                print(t)
                if t == request.user:
                    post.Likes.remove(request.user)
                    c=post.Likes.count()
                    post.Total_likes=c
                    post.save()
                    like=0
                    
                    break
                else:
                    post.Likes.add(request.user)
                    c=post.Likes.count()
                    post.Total_likes=c
                    post.save()
                    like=1
        return JsonResponse({'lk':like,'likecount':c})
    pass

@login_required(login_url='login')
def comment(request,id):
    try:
        pst=Post.objects.get(id=id)
        cmts=Comment.objects.filter(PID=pst.id)
        return render(request,'comment.html',{'cmt':cmts,'post':pst})
    except:
        return render(request,'comment.html')

@login_required(login_url='login')
def commentreact(request):
    if request.method == 'POST':
        post_id=request.POST.get('pid')
    
        post=Comment.objects.get(id=post_id)  #post means comment
        allLikes=post.commentlike.all()
        print(allLikes)
        if len(allLikes) == 0:
            post.commentlike.add(request.user)
            c=post.commentlike.count()
            post.Total_likes=c
            post.save()
            like=1
        else:
            for t in allLikes:
                print(t)
                if t == request.user:
                    post.commentlike.remove(request.user)
                    c=post.commentlike.count()
                    post.Total_likes=c
                    post.save()
                    like=0
                    
                    break
                else:
                    post.commentlike.add(request.user)
                    c=post.commentlike.count()
                    post.Total_likes=c
                    post.save()
                    like=1
        return JsonResponse({'lk':like,'likecount':c})

def mycomment(request):
    if request.method == 'POST':
        cmt=request.POST.get('comment')
        pid=request.POST.get("myid")

        current_post=Post.objects.get(id=pid)
        ac=Account.objects.get(user=request.user)
        
        x=Comment(userid=request.user,PID=current_post,cmt=cmt,userac=ac)
        x.save()
        return comment(request,pid)
    return JsonResponse({'res':'ok'})


def deletepost(request,id):
    # if request.method == 'POST':
        usr=request.user
        pst=Post.objects.get(id=id)
        if usr == pst.UID:
            pst.delete()
        return redirect('/profile/'+str(request.user.id))
        

def search(request,term):
    qs = Account.objects.all()
    for t in term.split():
        qs = qs.filter( Q(Name__icontains = t))
    return render(request,'search.html',{'q':qs})

def edit(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        img=request.FILES.get('image')
        phone=request.POST.get('phone')
        bio=request.POST.get('bio')

        usr=User.objects.get(id=request.user.id)

        x=Account.objects.get(user=usr)

        if name != '':
            x.Name=name
        if img != None:
            x.profile_picture=img
        if phone != '':
            x.phone = phone
        if bio != '':
            x.Bio=bio
        x.save()
        return profile(request,request.user.id)
    return render(request,'edit.html')

def lout(request):
    logout(request) 
    return index(request)

def share(request,id):
    x=Post.objects.get(id=id)
    return render(request,'post.html',{"i":x})
