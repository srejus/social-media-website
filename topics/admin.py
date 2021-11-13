from django.contrib import admin

from topics.models import Topic, Topic_follow

# Register your models here.
admin.site.register(Topic_follow)
admin.site.register(Topic)
