# Generated by Django 2.0.2 on 2018-12-07 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backmanage', '0005_auto_20181206_1437'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dianzhanhf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Huifu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hf_text', models.CharField(max_length=256)),
                ('hf_dianzhan', models.IntegerField()),
                ('hf_riqi', models.DateField()),
                ('hf_pinglunid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backmanage.Pinglun')),
                ('hf_uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backmanage.User')),
            ],
        ),
        migrations.AlterField(
            model_name='dianzhan',
            name='dz_plid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backmanage.Pinglun'),
        ),
        migrations.AlterField(
            model_name='dianzhan',
            name='dz_tid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backmanage.Tiezi'),
        ),
        migrations.AlterField(
            model_name='dianzhan',
            name='dz_uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backmanage.User'),
        ),
        migrations.AddField(
            model_name='dianzhanhf',
            name='dz_hfid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backmanage.Huifu'),
        ),
        migrations.AddField(
            model_name='dianzhanhf',
            name='dz_tid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backmanage.Tiezi'),
        ),
        migrations.AddField(
            model_name='dianzhanhf',
            name='dz_uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backmanage.User'),
        ),
    ]
