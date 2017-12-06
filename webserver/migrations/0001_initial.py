# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='cabinet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='名称', max_length=30)),
                ('power', models.CharField(verbose_name='权限', max_length=20)),
            ],
            options={
                'db_table': 'cabinet',
            },
        ),
        migrations.CreateModel(
            name='hostinfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('hostname', models.CharField(verbose_name='主机名', max_length=255)),
                ('IP', models.CharField(verbose_name='IP地址', max_length=50)),
                ('Mem', models.IntegerField(verbose_name='内存')),
                ('CPU', models.CharField(verbose_name='cpu', max_length=255)),
                ('CPUS', models.IntegerField(verbose_name='cpus')),
                ('OS', models.CharField(verbose_name='os', max_length=255)),
                ('virtual1', models.CharField(verbose_name='virtual', max_length=255)),
                ('status', models.CharField(verbose_name='状态', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('service_name', models.CharField(verbose_name='服务名称', max_length=20)),
                ('pid', models.IntegerField(verbose_name='pid')),
                ('module_letter', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='webserver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('phone', models.CharField(verbose_name='手机', max_length=20)),
                ('user_role', models.CharField(verbose_name='角色', max_length=40)),
                ('user', models.OneToOneField(verbose_name='用户', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
