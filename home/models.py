from django.contrib.auth.models import User
from django.db import models
from topics.models import Topic

# Create your models here.
class Account(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    Name=models.CharField(max_length=100,null=True,blank=True)
    Email=models.CharField(max_length=100,null=True,blank=True)
    phone=models.CharField(max_length=12,blank=True,null=True)
    profile_picture=models.ImageField(null=True,blank=True)
    Place=models.CharField(max_length=100,null=True,blank=True)
    Bio=models.TextField(null=True,blank=True)
    verified=models.BooleanField(default=False)
    def __str__(self): 
        rt=self.user.username+' ('+self.Name+')'
        return rt

class Post(models.Model):
    UID=models.ForeignKey(User,on_delete=models.CASCADE,related_name='uid')
    Time=models.DateTimeField(auto_now=True)
    posted_time = models.CharField(max_length=250,null=True,blank=True)
    user=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='uid')
    Img=models.ImageField(upload_to="images",null=True,blank=True)
    Caption=models.TextField(null=True,blank=True)
    Likes=models.ManyToManyField(User,related_name='Post',null=True,blank=True)
    Total_likes=models.IntegerField(null=True,blank=True,default=0)
    post_topic = models.CharField(max_length=250,null=True,blank=True)
    post_content = models.TextField(default="")

    def isLiked(self,request):
        if Post.objects.filter(id=self.id).filter(Likes=request.user).exists():
            return 1
        else:
            return 0

class Comment(models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE,related_name='cmtuid')
    PID=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='pid')
    Time=models.DateTimeField(auto_now=True)
    cmt=models.CharField(max_length=500,null=True,blank=True)
    userac=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='userac')
    commentlike=models.ManyToManyField(User,related_name='cmtlike',null=True,blank=True)
    Total_likes=models.IntegerField(null=True,blank=True,default=0)




class Following(models.Model):
    Bywho=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='follower')#aru follow cheyunnu
    whom=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='following')#are follow cheyunnu


class Blog(models.Model):
    title = models.CharField(max_length=250)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField(null=True,blank=True)
    Time=models.DateTimeField(auto_now=True)
    posted_time = models.CharField(max_length=250,null=True,blank=True)

    def __str__(self):
        return self.title

