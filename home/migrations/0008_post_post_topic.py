# Generated by Django 3.2.8 on 2021-11-14 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_account_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_topic',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]