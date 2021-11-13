
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Topic(models.Model):
    topic_name = models.CharField(max_length=250)

    def __str__(self):
        return self.topic_name

class Topic_follow(models.Model):
    topic_id = models.ForeignKey(Topic,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)