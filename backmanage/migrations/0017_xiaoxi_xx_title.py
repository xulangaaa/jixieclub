# Generated by Django 2.0.2 on 2019-01-23 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backmanage', '0016_xiaoxi'),
    ]

    operations = [
        migrations.AddField(
            model_name='xiaoxi',
            name='xx_title',
            field=models.CharField(default=0, max_length=32),
            preserve_default=False,
        ),
    ]
