# Generated by Django 2.0.2 on 2019-01-23 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backmanage', '0017_xiaoxi_xx_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xiaoxi',
            name='xx_fauid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backmanage.User'),
        ),
        migrations.AlterField(
            model_name='xiaoxi',
            name='xx_uid',
            field=models.IntegerField(),
        ),
    ]
