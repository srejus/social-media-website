from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('login',views.Login,name='login'),
    path('signup',views.signup,name='signup'),
    path('profile/<int:id>',views.profile,name='profile'),
    path('follow/<int:id>',views.follow,name='follow'),
    path('upload',views.upload,name='upload'),
    path('react',views.react,name='react'),
    path('comment/<int:id>',views.comment,name='comment'),
    path('commentreact',views.commentreact,name='commentreact'),
    path('mycomment',views.mycomment,name="mycomment"),
    path('deletepost/<int:id>',views.deletepost,name='deletepost'),
    path('search/<str:term>',views.search,name='search'),
    path('edit',views.edit,name='edit'),
    path('logout',views.lout,name='lout'),
    path('commentdelete',views.commentdelete,name='commentdelete'),
    # path('mail',views.mail,name='mail'),
    path("post/<int:id>",views.share,name='share'),
    path('following/<int:id>',views.followg,name='followg'),
    path('followers/<int:id>',views.followers,name='followers'),
]