from django.db import models
from datetime import *
from django.contrib.auth.models import User
class webserver(models.Model):
    user = models.OneToOneField(User,unique=True,verbose_name=('用户'))
    phone = models.CharField(u'手机',max_length=20)
    user_role = models.CharField(u'角色',max_length=40)

class cabinet(models.Model):
    name = models.CharField(u'名称',max_length=30)
    power = models.CharField(u'权限',max_length=20)
    class Meta:
        db_table = "cabinet"

class hostinfo(models.Model):
    hostname = models.CharField(u'主机名',max_length=255)
    IP = models.CharField(u'IP地址',max_length=50)
    Mem = models.IntegerField(u'内存')
    CPU = models.CharField(u'cpu',max_length=255)
    CPUS = models.IntegerField(u'cpus')
    OS = models.CharField(u'os',max_length=255)
    virtual1 = models.CharField(u'virtual',max_length=255)
    status = models.CharField(u'状态',max_length=50)

    def __str__(self):
        return self.hostname

class product(models.Model):
    service_name = models.CharField(u'服务名称',max_length=20)
    pid = models.IntegerField(u'pid')
    module_letter = models.CharField(max_length=10)
    class Meta:
        db_table = "product"

class monitorMemory(models.Model):
    hostid = models.IntegerField(u'监控主机ID')
    avai = models.CharField(u'空闲内存',max_length=20)
    total = models.CharField(u'总内存',max_length=20)
    ratio = models.CharField(u'使用率',max_length=20)
    time = models.DateTimeField(u'时间',auto_now_add=True)