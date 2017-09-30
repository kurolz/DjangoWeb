from django.db import models
from datetime import *
from django.contrib.auth.models import User

class webserver(models.Model):
    user = models.OneToOneField(User,unique=True,verbose_name=('用户'))
    phone = models.CharField('手机',max_length=20)
    user_role = models.CharField('角色',max_length=40)

class cabinet(models.Model):
    name = models.CharField('名称',max_length=30)
    power = models.CharField('权限',max_length=20)
    class Meta:
        db_table = "cabinet"

class server(models.Model):
    int_ip = models.CharField('内网IP地址',max_length=50)
    ext_ip = models.CharField('外网IP地址', max_length=50)
    mac_address = models.CharField('MAC地址',max_length=50)
    hostname = models.CharField('主机名',max_length=50)
    os = models.CharField('系统',max_length=50)
    status = models.IntegerField('状态')
    gateway = models.CharField('网关',max_length=50)
    cpu_model = models.CharField('CPU型号',max_length=100)
    cpu_thread_number = models.PositiveIntegerField('CPU线程数')
    server_disk = models.CharField('磁盘',max_length=20)
    server_mum = models.IntegerField('内存')
    manufacture_date = models.DateField('生产日期')
    manufacturers = models.CharField('生产商',max_length=30)
    cabinet_id = models.IntegerField('机柜ID')
    server_run = models.CharField('运行的服务',max_length=30)
    class Meta:
        db_table = "server"

class product(models.Model):
    service_name = models.CharField('服务名称',max_length=20)
    pid = models.IntegerField('pid')
    module_letter = models.CharField(max_length=10)
    class Meta:
        db_table = "product"

# class role(models.Model):
#     role = models.CharField('角色',max_length=40)
#     power = models.CharField('权限',max_length=40)
#
# class power(models.Model):
#     power_name = models.CharField('权限名称',max_length=40)
#     power_url = models.CharField('url', max_length=40)
