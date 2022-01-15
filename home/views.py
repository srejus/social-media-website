from os import uname
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import logout

from home.extra.comment import comment_delete
from topics.models import Topic, Topic_follow
from . feeds import feeds
from . models import *
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.views.decorators.csrf import csrf_exempt

from .extra import comment
from datetime import datetime

from twilio.rest import Client

import random,math


import smtplib

from django.db.models import Q 

#Image Compression
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def send_mail(to,msg):
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login('memail@gmail.com', '************')
            server.sendmail('memail@gmail.com', to, msg)
            return 0

def send_otp(to,msg):
    try:
            
            body = "Your OTP for Zero is ",str(msg)
           
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login('deliveryfoodeato@gmail.com', 'FoodeatoOnline.123')
            
            server.sendmail('deliveryfoodeato@gmail.com',to,str(body))
            
            return 0
    except:
        pass
        
# def send_otp(number,otp):

#     # Your Account SID from twilio.com/console
#     account_sid = "AC281598eccfe4d2fb5f431116b85b6ab3"
#     # Your Auth Token from twilio.com/console
#     auth_token  = "d2586055b46b0aa38dd35f57f6dc2ab2"

#     client = Client(account_sid, auth_token)

#     message = client.messages.create(
#         to="+91"+str(number), 
#         from_="+13205476036",
#         body="Your OTP:"+str(otp))


def generateOTP() :
 
    # Declare a digits variable 
    # which stores all digits
    digits = "0123456789"
    OTP = ""
 
   # length of password can be changed
   # by changing value in range
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP

def generatePassword():
    chars = "0123456789abcdtesfjghsbnbb.>,L;HysbcjsV~`'=+/?"
    password = ""
 
   # length of password can be changed
   # by changing value in range
    for i in range(8) :
        password += chars[math.floor(random.random() * 10)]
 
    return password



# def mail(request):
#             message = 'Subject: {}\n\n{}'.format('SUBJECT',' Hello  this is a mail')
#             send_mail('to@gmail.com',message)
#             return JsonResponse({'res':'wee'})
# Create your views here.

@login_required(login_url='login')
def index(request):
    id=request.user.id
    #Topics
    tpc = Topic.objects.all()
    if Following.objects.filter(Bywho=id).exists():
        myfeeds=feeds.feedalgo(id)
        suggest_feeds=feeds.suggestalgo(id)
        topic_feed = feeds.topic_algo(id)
        
        

        return render(request,'index.html',{'myfeed':myfeeds,'sf':suggest_feeds,'tf':topic_feed,'tp':tpc})
    else:
        suggest_feeds=feeds.suggestalgo(id)
        x=Account.objects.order_by('?')[:11]
        return render(request,'index.html',{'sf':suggest_feeds,'tp':tpc})

def reader(request,id):
    post = Post.objects.get(id=id)
    return render(request,'read.html',{'pst':post})

def Login(request):
    if request.method=='POST':
        username=request.POST.get("username")

        
        otp = generateOTP()

        o=str(otp)
        
        send_otp(username,o)
        # print("OTP:",otp)
        # signup(request,username)
        
        # # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     login(request, user)
  
        # else:
        #     messages.warning(request,'Password or Username does not match!')
        #     return render(request,'login.html')
        return render(request,'opt.html',{'ot':otp,'u':username})
    return render(request,'login.html')
def otp(request):
    if request.method == 'POST':
        real_otp = request.POST.get('otpRel')
        inp_otp = request.POST.get('otpEnter')
        username = request.POST.get('uname')
        
        if real_otp == inp_otp:
            #code for fetch password and login or signup
            if User.objects.filter(username=username).exists():
                pw = generatePassword()
                
                u = User.objects.get(username=username)
                u.set_password(pw)
                u.save()

                #login code

                user = authenticate(username=username, password=pw)
                if user is not None:
                    login(request,user)
                    return redirect('edit')
                else:
                    return Login(request)

                return redirect('/')
            else:
                mail = str(username)+'@zero.com'
                pw = generatePassword()
                user = User.objects.create_user(username, mail, pw)
                user.save()

                x=Account(user=user,phone=username)
                x.save()
                #login code

                user = authenticate(username=username, password=pw)
                if user is not None:
                    login(request,user)
                    return redirect('edit')
                else:
                    return Login(request)
                return redirect('/')
    return render(request,'opt.html')

def signup(request,username):
    #Code to Create an Account
    return render(request, 'opt.html')

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
#    print(id)
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
        content = request.POST.get('content')
        topic = request.POST.get('topic')
        img=request.FILES.get('image')

        

        # compress the image here and then save it
        try:
            i = Image.open(img)
            thumb_io = BytesIO()
            i.save(thumb_io, format='JPEG', quality=70)
            inmemory_uploaded_file = InMemoryUploadedFile(thumb_io, None, str(img), 
                                                'image/jpeg', thumb_io.tell(), None)
        except:
              pass
        #Find current time and date
        # datetime object containing current date and time
        now = datetime.now()
        
    
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        

        curent_ac=Account.objects.get(user=request.user)

       # x=Post(UID=request.user,user=curent_ac,Caption=capt,Img=inmemory_uploaded_file,post_topic=topic,posted_time=dt_string)
        x = Post(UID=request.user,user=curent_ac,Caption=capt,post_topic=topic,posted_time=dt_string,post_content=content)
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

@csrf_exempt
def upload1(request):
    if request.method == 'POST':
        capt=request.POST.get('caption')
        topic = request.POST.get('topic')
        content = request.POST.get('content')
        img=request.FILES.get('image')

        

        # compress the image here and then save it
        try:
            i = Image.open(img)
            thumb_io = BytesIO()
            i.save(thumb_io, format='JPEG', quality=70)
            inmemory_uploaded_file = InMemoryUploadedFile(thumb_io, None, str(img), 
                                                'image/jpeg', thumb_io.tell(), None)
        except:
              pass
        #Find current time and date
        # datetime object containing current date and time
        now = datetime.now()
        
    
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        

        curent_ac=Account.objects.get(user=request.user)

       # x=Post(UID=request.user,user=curent_ac,Caption=capt,Img=inmemory_uploaded_file,post_topic=topic,posted_time=dt_string)
        x = Post(UID=request.user,user=curent_ac,Caption=capt,post_topic=topic,posted_time=dt_string,post_content=content)
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
        # print(allLikes)
        if len(allLikes) == 0:
            post.Likes.add(request.user)
            c=post.Likes.count()
            post.Total_likes=c
            post.save()
            like=1
        else:
            for t in allLikes:
                # print(t)
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

def commentdelete(request):
    if request.method == 'POST':
        idstr = request.POST.get('pid')
        id = int(idstr.replace('z',''))
        # print(idstr)
        #Code for remove a comment
        comment_delete(id)
        return JsonResponse({'res':'ok'})


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
        #print(allLikes)
        if len(allLikes) == 0:
            post.commentlike.add(request.user)
            c=post.commentlike.count()
            post.Total_likes=c
            post.save()
            like=1
        else:
            for t in allLikes:
                # print(t)
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


        #Topics

        tps = Topic.objects.all()
        tp_follow = Topic_follow.objects.filter(user_id = request.user.id)
    return render(request,'search.html',{'q':qs,'ts':tps,'tf':tp_follow})

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


def followg(request,id):
    #People who follow by the user

    res_un = Following.objects.filter(Bywho = id)
    
    res = []

    for i in res_un:
        res.append(i.whom)

    usrs = Account.objects.filter(user__in = res)
    
    return render(request,'search.html',{'q':usrs})


def followers(request,id):
    #People who followed  the user

    res_un = Following.objects.filter(whom = id)
    
    res = []

    for i in res_un:
        res.append(i.Bywho)
    
    usrs = Account.objects.filter(user__in = res)

    return render(request,'search.html',{'q':usrs})

    
