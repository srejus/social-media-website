# Generated by Django 3.2.8 on 2021-11-14 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='Time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='posted_time',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]