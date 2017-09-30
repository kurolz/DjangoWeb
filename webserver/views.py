# Create your views here.
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from webserver.forms import UserForm,RegisterForm,AlterForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import time
import socket
import platform
import json


#登录验证
def login(req):
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

#注销
@login_required
def logout(req):
    auth.logout(req)
    return HttpResponseRedirect('/webserver/login/')


'''获取本机IP'''
def getServerIp(request):
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return render(request, 'menu.html', {'myaddr':myaddr, })

'''获取访问的IP'''
def geThostIp(request):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return render(request, 'menu.html', {'hostip':'192.168.1.1' })

#用户列表
@login_required
def userList(req,id = 0):
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

#添加用户
@login_required
def userAdd(req):
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

#修改用户
@login_required
def userAlter(req, id):
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
#####
from django.db.models import Count,Sum
# @login_required
def serverList(request):
    if request.method == "POST":
        print(request.POST)
        pageSize = request.POST.get('pageSize')   # how manufactoryy items per page
        pageNumber = request.POST.get('pageNumber')
        offset = request.POST.get('offset')  # how many items in total in the DB
        search = request.POST.get('search')
        sort_column = request.POST.get('sort')   # which column need to sort
        order = request.POST.get('order')      # ascending or descending
        if search:    #    判断是否有搜索字
            all_records = User.objects.filter(id=search,asset_type=search,business_unit=search,idc=search)
        else:
            all_records = User.objects.all()   # must be wirte the line code here

        if sort_column:   # 判断是否有排序需求
            sort_column = sort_column.replace('asset_', '')
            if sort_column in ['id','asset_type','sn','name','management_ip','manufactory','type']:   # 如果排序的列表在这些内容里面
                if order == 'desc':   # 如果排序是反向
                    sort_column = '-%s' % (sort_column)
                all_records = User.objects.all().order_by(sort_column)
            elif sort_column in ['salt_minion_id','os_release',]:
                # server__ 表示asset下的外键关联的表server下面的os_release或者其他的字段进行排序
                sort_column = "server__%s" % (sort_column)
                if order == 'desc':
                    sort_column = '-%s'%(sort_column)
                all_records = User.objects.all().order_by(sort_column)
            elif sort_column in ['cpu_model','cpu_count','cpu_core_count']:
                sort_column = "cpu__%s" %(sort_column)
                if order == 'desc':
                    sort_column = '-%s'%(sort_column)
                all_records = User.objects.all().order_by(sort_column)
            elif sort_column in ['rams_size',]:
                if order == 'desc':
                    sort_column = '-rams_size'
                else:
                    sort_column = 'rams_size'
                all_records = User.objects.all().annotate(rams_size = Sum('ram__capacity')).order_by(sort_column)
            elif sort_column in ['localdisks_size',]:  # using variable of localdisks_size because there have a annotation below of this line
                if order == "desc":
                    sort_column = '-localdisks_size'
                else:
                    sort_column = 'localdisks_size'
                #     annotate 是注释的功能,localdisks_size前端传过来的是这个值，后端也必须这样写，Sum方法是django里面的，不是小写的sum方法，
                # 两者的区别需要注意，Sum（'disk__capacity‘）表示对disk表下面的capacity进行加法计算，返回一个总值.
                all_records = User.objects.all().annotate(localdisks_size=Sum('disk__capacity')).order_by(sort_column)

            elif sort_column in ['idc',]:
                sort_column = "idc__%s" % (sort_column)
                if order == 'desc':
                    sort_column = '-%s'%(sort_column)
                all_records = User.objects.all().order_by(sort_column)

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
        for user_li in pageinator.page(page):
            response_data['rows'].append({
                "username": user_li.username if user_li.username else "",
                "email":user_li.email if user_li.email else "",
                "is_active":user_li.is_active if user_li.is_active else "",
                "last_login": user_li.last_login.strftime("%Y-%m-%d %H:%M") if user_li.last_login else "",
            })
        return HttpResponse(json.dumps(response_data))
    return render(request, 'serverlist.html')
