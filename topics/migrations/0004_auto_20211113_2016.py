# Generated by Django 3.2.8 on 2021-11-13 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topics', '0003_auto_20211113_2007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic_follow',
            name='user_id',
        ),
        migrations.AddField(
            model_name='topic_follow',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
