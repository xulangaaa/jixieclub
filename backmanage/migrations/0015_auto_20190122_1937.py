# Generated by Django 2.0.2 on 2019-01-22 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backmanage', '0014_huifu_hf_huifu_uid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='huifu',
            name='hf_huifu_uid',
        ),
        migrations.AddField(
            model_name='huifu',
            name='hf_huifu_uname',
            field=models.CharField(max_length=64, null=True),
        ),
    ]