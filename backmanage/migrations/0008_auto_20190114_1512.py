# Generated by Django 2.0.2 on 2019-01-14 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backmanage', '0007_user_u_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='u_gexingqianming',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='u_nicheng',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
