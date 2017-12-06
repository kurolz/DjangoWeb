# Create your views here.
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from webserver.forms import UserForm,RegisterForm,AlterForm,hostadimnForm,monitorForm,autoArrMinionForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Count,Sum
from .models import hostinfo
from django.http import JsonResponse
from django.core import serializers
from .models import monitorMemory
import urllib.request, urllib.parse, urllib.request
import salt.client
import time
import socket
import platform
import sys,os
import json
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def page_not_found(request):
    '''
    404报错页面
    '''
    return render(request,'404.html')

def page_error(request):
    '''
    500报错页面
    '''
    return render(request,'500.html')

def login(req):
    '''
    登录验证
    '''
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if req.method == 'GET':
        uf = UserForm()
        return render(req,'login.html', {'uf': uf,'nowtime': nowtime })
    else:
        uf = UserForm(req.POST)
        if uf.is_valid():
            username = req.POST.get('username', '')
            password = req.POST.get('password', '')
            user = auth.authenticate(username = username,password = password)
            if user is not None and user.is_active:
                auth.login(req,user)
                return render(req, 'index.html')
            else:
                return render(req, 'login.html', {'uf': uf,'nowtime': nowtime, 'password_is_wrong': True})
        else:
            return render(req, 'login.html', {'uf': uf,'nowtime': nowtime })

@login_required
def index(req):
    system = platform.system()
    if system == 'Windows':
        version = platform.version()
        OsVersion = system + '. '+ version
    else:
        node = platform.node()
        OsVersion = node + '@' + system
    return render(req, 'index.html', {'OsVersion': OsVersion})

@login_required
def logout(req):
    '''
    注销
    '''
    auth.logout(req)
    return HttpResponseRedirect('/webserver/login/')

def getServerIp(request):
    '''
    获取本机IP
    '''
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return render(request, 'menu.html', {'myaddr':myaddr, })

def geThostIp(request):
    '''
    获取访问的IP
    '''
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return render(request, 'menu.html', {'hostip':'192.168.1.1' })

@login_required
def userList(req,id = 0):
    '''
    用户列表
    '''
    if id != 1:
        User.objects.filter(id = id).delete()
    users = User.objects.all()  #导入User表
    after_range_num = 2     #当前页前显示2页
    befor_range_num = 2     #当前页后显示2页
    try:    #如果请求的页码少于1或者类型错误，则跳转到第1页
        page = int(req.GET.get("page",1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    paginator = Paginator(users,11)   #每页显示11
    try:  # 跳转到请求页面，如果该页不存在或者超过则跳转到尾页
        users_list = paginator.page(page)
    except(EmptyPage, InvalidPage, PageNotAnInteger):
        users_list = paginator.page(paginator.num_pages)
    if page >= after_range_num:
        page_range = paginator.page_range[page - after_range_num:page + befor_range_num]
    else:
        page_range = paginator.page_range[0:int(page) + befor_range_num]
    return render(req,'userlist.html',{'user_list':users_list,'page_range': page_range})

@login_required
def userAdd(req):
    '''
    添加用户
    '''
    if req.method == "POST":
        user_add = RegisterForm(req.POST)
        if user_add.is_valid():
            data = user_add.cleaned_data
            print (data)
            add_user = data.get('add_user')
            add_password = data.get('add_password')
            add_email = data.get('add_email', '')
            add_isactive = data.get('add_isactive')
            user = User()
            user.username = add_user
            user.set_password(add_password)
            user.email = add_email
            user.is_active = add_isactive
            user.save()
            return render(req, 'useradd.html', {'add_newuser': add_user})
        else:
            errors = user_add.errors
            return render(req, 'useradd.html',{'add_FormInput': user_add,'errors': errors})
    else:
        user_add = RegisterForm()
    return render(req, 'useradd.html', {'add_FormInput': user_add})

@login_required
def userAlter(req, id):
    '''
    修改用户
    '''
    user_alter = AlterForm(req.POST)
    if req.method == "POST":
        if user_alter.is_valid():
            alter_data = user_alter.cleaned_data
            print(alter_data)
            alter_email = alter_data.get('alter_email')
            alter_isactive = alter_data.get('alter_isactive')
            alt = User.objects.get(id=id)
            alt.email = alter_email
            alt.is_active = alter_isactive
            alt.save()
            return HttpResponseRedirect('/webserver/user/list/')
        else:
            errors = user_alter.errors
            return render(req, 'useralter.html', {'alter_FormInput': user_alter, 'errors': errors})
    else:
        try:
            UpdateUser = User.objects.only('username').get(id=id).username
            old_eamil = User.objects.only('email').get(id=id).email
            old_is_active = User.objects.only('is_active').get(id=id).is_active
            if old_is_active:
                old_is_active = 1
            else:
                old_is_active = 0

            form = AlterForm(
                initial={'alter_email': old_eamil}
            )
            return render(req, 'useralter.html', {'alter_FormInput': form, 'UpdateUser': UpdateUser, 'alter_is_active':old_is_active})
        except:
            post = get_object_or_404(User, id=id)
            form = AlterForm(instance=post)
            return render(req, 'useralter.html', {'form': form})

@login_required
def serverList(request,id = 0):
    '''
    服务器列表
    '''
    if id != 0:
        hostinfo.objects.filter(id = id).delete()
    if request.method == "POST":
        getHostInfo()
        print(request.POST)
        pageSize = request.POST.get('pageSize')   # how manufactoryy items per page
        pageNumber = request.POST.get('pageNumber')
        offset = request.POST.get('offset')  # how many items in total in the DB
        search = request.POST.get('search')
        sort_column = request.POST.get('sort')   # which column need to sort
        order = request.POST.get('order')      # ascending or descending
        if search:    #    判断是否有搜索字
            all_records = hostinfo.objects.filter(id=search,asset_type=search,business_unit=search,idc=search)
        else:
            all_records = hostinfo.objects.all()   # must be wirte the line code here

        if sort_column:   # 判断是否有排序需求
            sort_column = sort_column.replace('asset_', '')
            if sort_column in ['id','asset_type','sn','name','management_ip','manufactory','type']:   # 如果排序的列表在这些内容里面
                if order == 'desc':   # 如果排序是反向
                    sort_column = '-%s' % (sort_column)
                all_records = hostinfo.objects.all().order_by(sort_column)
            elif sort_column in ['salt_minion_id','os_release',]:
                # server__ 表示asset下的外键关联的表server下面的os_release或者其他的字段进行排序
                sort_column = "server__%s" % (sort_column)
                if order == 'desc':
                    sort_column = '-%s'%(sort_column)
                all_records = hostinfo.objects.all().order_by(sort_column)
            elif sort_column in ['cpu_model','cpu_count','cpu_core_count']:
                sort_column = "cpu__%s" %(sort_column)
                if order == 'desc':
                    sort_column = '-%s'%(sort_column)
                all_records = hostinfo.objects.all().order_by(sort_column)
            elif sort_column in ['rams_size',]:
                if order == 'desc':
                    sort_column = '-rams_size'
                else:
                    sort_column = 'rams_size'
                all_records = hostinfo.objects.all().annotate(rams_size = Sum('ram__capacity')).order_by(sort_column)
            elif sort_column in ['localdisks_size',]:  # using variable of localdisks_size because there have a annotation below of this line
                if order == "desc":
                    sort_column = '-localdisks_size'
                else:
                    sort_column = 'localdisks_size'
                #     annotate 是注释的功能,localdisks_size前端传过来的是这个值，后端也必须这样写，Sum方法是django里面的，不是小写的sum方法，
                # 两者的区别需要注意，Sum（'disk__capacity‘）表示对disk表下面的capacity进行加法计算，返回一个总值.
                all_records = hostinfo.objects.all().annotate(localdisks_size=Sum('disk__capacity')).order_by(sort_column)

            elif sort_column in ['idc',]:
                sort_column = "idc__%s" % (sort_column)
                if order == 'desc':
                    sort_column = '-%s'%(sort_column)
                all_records = hostinfo.objects.all().order_by(sort_column)

            elif sort_column in ['trade_date','create_date']:
                if order == 'desc':
                    sort_column = '-%s'%sort_column
                all_records = User.objects.all().order_by(sort_column)

        all_records_count=all_records.count()

        if not offset:
            offset = 0
        if not pageSize:
            pageSize = 10    # 默认是每页20行的内容，与前端默认行数一致
        pageinator = Paginator(all_records, pageSize)   # 开始做分页
        page = int(int(offset) / int(pageSize) + 1)
        response_data = {'total': all_records_count, 'rows': []}
        for server_li in pageinator.page(page):
            response_data['rows'].append({
                "id": server_li.id if server_li.id else "",
                "hostname": server_li.hostname if server_li.hostname else "",
                "IP":server_li.IP if server_li.IP else "",
                "Mem":server_li.Mem if server_li.Mem else "",
                "CPU": server_li.CPU if server_li.CPU else "",
                "CPUS": server_li.CPUS if server_li.CPUS else "",
                "OS": server_li.OS if server_li.OS else "",
                "virtual1": server_li.virtual1 if server_li.virtual1 else "",
                "status": server_li.status if server_li.status else "",
            })
        return HttpResponse(json.dumps(response_data))
    return render(request, 'serverlist.html')

def getHostInfo():
    ### salt调用 ###
    # local = salt.client.LocalClient() # api
    ### 目标主机指定 ###
    tgt = "*"
    ### 获取grains，disk信息 ###
    # grains = local.cmd(tgt,"grains.items") # api
    (status, grains_return) = subprocess.getstatusoutput(" ssh 127.0.0.1 'salt \"*\" --out raw grains.items' ")
    grains = eval(grains_return.replace('}}\n{','},'))
    # diskusage = local.cmd(tgt,"disk.usage") # api
    (status, diskusage) = subprocess.getstatusoutput(" ssh 127.0.0.1 'salt \"*\" --out raw disk.usage' ")
    diskusage = eval(diskusage.replace('}}\n{', '},'))
    for i in grains.keys():
        try:
            ###去掉127.0.0.1这个地址
            hostname = grains[i]["nodename"]
            ip = str(grains[i]["ipv4"]).strip('[]')
            ip = ip.replace("\'", "")
            ip = ip.replace("127.0.0.1,", "")
            ip = ip.replace(", 127.0.0.1", "")
            ip = ''.join(ip.split())
            ip = ip.replace(",", " | ")
            mem = grains[i]["mem_total"] / 1024 + 1
            num_cpu = grains[i]["num_cpus"]
            OS = grains[i]["os"] + ' ' + grains[i]["osrelease"]
            cpu = grains[i]["cpu_model"]
            virtual1 = grains[i]["virtual"]
            status = '连接'
            #磁盘容量
            if "/" not in diskusage[i]:
                disk_used = " "
                disk_capacity = " "
            else:
                disk_used = float(diskusage[i]["/"]["1K-blocks"]) / 1048576
                disk_capacity = diskusage[i]["/"]["capacity"]
            if "/data" not in diskusage[i]:
                disk_data_used = " "
                disk_data_capacity = " "
            else:
                disk_data_used = float(diskusage[i]["/data"]["1K-blocks"]) / 1048576
                disk_data_capacity = diskusage[i]["/data"]["capacity"]

            if "/data1" not in diskusage[i]:
                disk_data1_used = " "
                disk_data1_capacity = " "
            else:
                disk_data1_used = float(diskusage[i]["/data"]["1K-blocks"]) / 1048576
                disk_data1_capacity = diskusage[i]["/data"]["capacity"]

                ####获取网卡mac信息####
            # if "eth0" not in grains[i]["hwaddr_interfaces"]:
            #     eth0=" "
            # else:
            #     eth0=grains[i]["hwaddr_interfaces"]["eth0"]
            #
            # if "eth1" not in grains[i]["hwaddr_interfaces"]:
            #     eth1=" "
            # else:
            #     eth1=grains[i]["hwaddr_interfaces"]["eth1"]

            grains[i]["hwaddr_interfaces"].pop("lo")
            hostnames = hostinfo.objects.values_list('hostname', flat=True) # 获取资产列表中的主机名
            if hostnames:
                if hostname in hostnames:  ##判断主机是否已经入库，如果存在输出提示，不存在则入库
                    hostinfoupdate = hostinfo.objects.get(hostname=hostname)
                    hostinfoupdate.hostname = hostname
                    hostinfoupdate.IP = ip
                    hostinfoupdate.Mem = mem
                    hostinfoupdate.CPU = cpu
                    hostinfoupdate.CPUS = num_cpu
                    hostinfoupdate.OS = OS
                    hostinfoupdate.virtual1 = virtual1
                    hostinfoupdate.status = status
                    hostinfoupdate.save()
                else:
                    hostinfoadd = hostinfo()
                    hostinfoadd.hostname = hostname
                    hostinfoadd.IP = ip
                    hostinfoadd.Mem = mem
                    hostinfoadd.CPU = cpu
                    hostinfoadd.CPUS = num_cpu
                    hostinfoadd.OS = OS
                    hostinfoadd.virtual1 = virtual1
                    hostinfoadd.status = status
                    hostinfoadd.save()
            else:
                hostinfoadd = hostinfo()
                hostinfoadd.hostname = hostname
                hostinfoadd.IP = ip
                hostinfoadd.Mem = mem
                hostinfoadd.CPU = cpu
                hostinfoadd.CPUS = num_cpu
                hostinfoadd.OS = OS
                hostinfoadd.virtual1 = virtual1
                hostinfoadd.status = status
                hostinfoadd.save()
        except:
            hostnames = hostinfo.objects.values_list('hostname', flat=True) # 获取资产列表中的主机名
            if i in hostnames:
                hostinfoupstatus = hostinfo.objects.get(hostname=i)
                hostinfoupstatus.status = '未连接'
                hostinfoupstatus.save()
            continue

@login_required
def hostAdmin(request):
    '''
    批量执行命令
    '''
    if request.method == 'POST':
        # local = salt.client.LocalClient() # api
        search = hostadimnForm(request.POST)
        cmd_host = request.POST.get('hostlist', '')
        funlist = request.POST.get('funlist', '')
        command = request.POST.get('command','')
        if cmd_host == '':
            cmd_host = '*'
        if command != '':
            if '"' in command:
                command = command.replace('"',"'")
            (status, result) = subprocess.getstatusoutput(
                " ssh 127.0.0.1 'salt \"" + cmd_host + "\" " + funlist + " \" " + command + " \" ' ")
            # result = local.cmd(cmd_host, funlist, [command])  # api
        else:
            (status, result) = subprocess.getstatusoutput(
                " ssh 127.0.0.1 'salt \"" + cmd_host + "\" " + funlist + " ' ")
            # result = local.cmd(cmd_host, funlist) # api
        result_dict = {
            'search': search,
            'result': result,
        }
        return render(request, 'hostadmin.html', result_dict)

    else:
        search = hostadimnForm()
        result_dict = {
            'search' : search,
        }
        return render(request, 'hostadmin.html', result_dict)

def loginZabbix():
    '''
    登录zabbix获取session
    '''
    # url and url header
    # zabbix的api 地址，用户名，密码，这里修改为自己实际的参数
    zabbix_url = "http://www.mykurol.com:8088/api_jsonrpc.php"
    # zabbix_header = {"Content-Type": "application/json"}
    zabbix_user = "Admin"
    zabbix_pass = "******"

    # 用户认证信息的部分，最终得到一个sessionID
    # 这里是生成一个json格式的数据，用户名和密码
    auth_data = json.dumps({
        "jsonrpc": "2.0",
        "method": "user.login",
        "params":
            {
                "user": zabbix_user,
                "password": zabbix_pass
            },
        "id": 0
    })

    # 认证，获取session
    auth_value = auth_data.encode('utf-8')
    auth_request = urllib.request.Request(zabbix_url, auth_value)
    auth_request.add_header('Content-Type', 'application/json')
    auth_response = urllib.request.urlopen(auth_request)
    auth_result = json.loads(auth_response.read())
    session = auth_result['result']  # 获取到的有效用户身份验证令牌
    return [zabbix_url,session]

@login_required
def getMonitor(request):
    '''获取zabbix监控的主机列表'''
    monitorform = monitorForm()
    zabbix_host_info = dataHandle(func=getZabbixHost)
    monitor_hostnames = []
    cpuutils_now = ''
    cpuload_now = ''
    fsused_now = ''
    fsfree_now = ''
    for i in zabbix_host_info:
        monitor_hostid = i['hostid']
        monitor_hostname = i['host']
        monitor_hostnames = monitor_hostnames + [(monitor_hostid, monitor_hostname)]
    host_num  = len(monitor_hostnames)
    monitorform.fields['monitorHost'].choices = monitor_hostnames

    '''获取提交的主机ID'''
    try:
        if request.method == "POST":
            if "monitorHost" in request.POST:   # name为monitorHost的表单提交
                hostid = request.POST.get('monitorHost','')
            else:
                hostid = 10084
        else:
            hostid = 10084

        '''获取提交主机的itemids'''
        # itemids = dataHandle(func=getZabbixitem,hostid=hostid)

        '''获取CPU使用率'''
        cpuutils_dict = dataHandle(func=getZabbixCPUutil, hostid=hostid)

        '''获取CPU负载'''
        cpuload_dict = dataHandle(func=getZabbixCPUload, hostid=hostid)

        '''获取硬盘使用量'''
        fsused_dict = dataHandle(func=getfsused, hostid=hostid)

        '''获取硬盘总量'''
        fsfree_dict = dataHandle(func=getfsfree, hostid=hostid)

        for i in cpuutils_dict:
            cpuutils_now = i['prevvalue']  # CPU当前使用率百分比
        for i in cpuload_dict:
            cpuload_now = i['prevvalue']  # CPU当前负载百分比
        for i in fsused_dict:
            fsused_now = i['prevvalue'] # 磁盘使用量
        for i in fsfree_dict:
            fsfree_now = i['prevvalue'] # 磁盘空闲

    except KeyError as e:
        print (e)
        pass

    '''获取内存使用率最后15次的数据'''
    me_data = monitorMemory.objects.filter(hostid=hostid)[2:]
    '''返回的前端的字典'''
    monitor_dict = {
        "monitorform" : monitorform,    # 监控主机的表单
        "monitor_hostnames" : monitor_hostnames, # 监控的主机的下拉菜单列表
        "host_num" : host_num,    # 监控的主机个数
        "cpuutils_now" : cpuutils_now,  # CPU当前使用率
        "cpuload_now" : cpuload_now,    # CPU当前负载
        "fsused_now" : fsused_now,  # 磁盘使用量
        "fsfree_now" : fsfree_now, # 磁盘空闲
        "data" : me_data
    }
    return render(request, 'Monitor.html', monitor_dict)

def dataHandle(*args,**kw):
    '''
    数据处理返回结果
    '''
    login_zabbix_relist = loginZabbix()
    zabbix_url = login_zabbix_relist[0]
    session = login_zabbix_relist[1]
    if len(kw.keys()) == 1:
        data = kw["func"](session=session)
    else:
            data = kw["func"](session=session,parameter=kw["hostid"])
    value = data.encode('utf-8')
    host_request = urllib.request.Request(zabbix_url, value)
    host_request.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(host_request)
    result = json.loads(response.read())
    return result['result']

def getZabbixHost(*args,**b):
    '''
    检索zabbix监控主机的提交data
    '''
    zabbix_host_data = json.dumps({
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": [
                "hostid",
                "host"
            ],
            "selectInterfaces": [
                "interfaceid",
                "ip"
            ]
        },
        "id": 2,
        "auth": b["session"]
    })
    return zabbix_host_data

def getZabbixitem(*args,**b):
    '''
    获取itemids的提交data
    '''
    itemids_data = json.dumps({
        "jsonrpc" : "2.0",
        "method": "item.get",
        "params": {
            "output": "itemids",
            "hostids": b["parameter"],
            "search": {
                "key_": "system.cpu.util"
           }
        },
        "auth": b["session"],
        "id": 0
    })
    return itemids_data

def getZabbixCPUutil(*args, **b):
    '''
    获取CPU使用率
    '''
    cpu_data = json.dumps({
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": "extend",
            "hostids": b["parameter"],
            "search": {
                "key_": "system.cpu.util" # 只查询key_包含“system.cpu.util”字段的item
            }
        },
        "auth": b["session"],
        "id": 2
    })
    return cpu_data

def getZabbixCPUload(*args, **b):
    '''
    获取CPU负载
    '''
    cpu_data = json.dumps({
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": "extend",
            "hostids": b["parameter"],
            "search": {
                "key_": "system.cpu.load"  # 只查询key_包含“system.cpu.load”字段的item
            }
        },
        "auth": b["session"],
        "id": 2
    })
    return cpu_data

def getfsused(*args, **b):
    '''
    获取磁盘使用量
    '''
    cpu_data = json.dumps({
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": "extend",
            "hostids": b["parameter"],
            "search": {
                "key_": "vfs.fs.size[/,used]"  # 只查询key_包含“vfs.fs.size[/,used]”字段的item
            }
        },
        "auth": b["session"],
        "id": 2
    })
    return cpu_data

def getfsfree(*args, **b):
    '''
    获取磁盘空闲
    '''
    cpu_data = json.dumps({
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": "extend",
            "hostids": b["parameter"],
            "search": {
                "key_": "vfs.fs.size[/, free]"
            }
        },
        "auth": b["session"],
        "id": 2
    })
    return cpu_data

def sendemail():
    '''
    邮件发送
    '''
    mail_host = "smtp.163.com"  # 设置smtp服务器，例如：smtp.163.com
    mail_user = "kurolz@163.com"  # 用户名
    mail_pass = "******"  # 密码

    sender = 'kurolz@163.com'  # 发送邮件
    receivers = 'kurolz@163.com'  # 接收邮件

    message = MIMEText('This is a Python Test Text')
    message['From'] = sender
    message['To'] = receivers

    subject = 'One Test Mail'
    message['Subject'] = Header(subject)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件" + str(e))

@login_required
def serverAdd(request):
    result = ''
    check_ip_inro = 0   #检查主机是否存在，0不存在，1存在
    if request.method == "POST":
        form = autoArrMinionForm(request.POST)
        if form.is_valid():
            ip = request.POST.get('add_ip') # 需要安装minion端的ip
            username = request.POST.get('add_username') # 需要安装minion端的用户名
            password = request.POST.get('add_password') # 需要安装minion端的密码
            check_ip_list = hostinfo.objects.values_list('IP', flat=True) # 获取已经安装minion的ip列表
            for i in check_ip_list:  # 将有多个ip的主机ip分开，自成一个列表供匹配检查主机是否已经存在
                if " | " in i:
                    check_ip_list_two = i.split(" | ")
                    if ip in check_ip_list_two: # 判断输入的ip是否在主机列表中
                        check_ip_inro = 1
                        break
            if ip not in check_ip_list and check_ip_inro == 0:
                try:
                    os.system("echo '"+ip+":'>> /etc/salt/roster && \
                                echo '  host: " +ip+ "'>> /etc/salt/roster && \
                                echo '  user: " +username+ "'>> /etc/salt/roster && \
                                echo '  passwd: " +password+ "'>> /etc/salt/roster && \
                                echo '  sudo: True'>> /etc/salt/roster && \
                                echo '  tty: True'>> /etc/salt/roster && \
                                echo '  timeout: 10'>> /etc/salt/roster")
                    os.system("salt-ssh '" + ip + "' -ir 'easy_install certifi'") # 安装cretifi模块
                    (status_gethostname, resultgethostname) = subprocess.getstatusoutput("salt-ssh -ir '" + ip + "' 'hostname'") # 获取hostname
                    os.system("salt-ssh '" + ip + "' -ir 'echo ''"+ip+"' '"+resultgethostname+"''>> /etc/hosts'") # 添加hosts
                    (status, result) = subprocess.getstatusoutput("salt-ssh -i '"+ip+"' state.sls minions.install") # 执行安装命令，并返回结果
                except:
                    result = "注意：无法连接该主机，请检查ip和用户密码是否正确！"
            else:
                result = "提示：这台主机已加入主机列表！"
        else:
            result = "注意：请填写正确的ip、用户名或密码！"
    else:
        form = autoArrMinionForm()
    re = {
        "form": form,
        "result": result
    }
    return  render(request, "serveradd.html", re)


