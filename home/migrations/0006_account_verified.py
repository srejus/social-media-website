# Generated by Django 3.1.12 on 2021-10-14 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_comment_total_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
