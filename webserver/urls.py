from django.conf.urls import *
from webserver import views
import DjangoWeb.settings
# from .views import  UserInfoUpdate
from webserver.views import login
from django.contrib.auth import views as user_views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^login/$',views.login),
    url(r'^index/$',views.index),
    url(r'^logout/$',views.logout),
    url(r'^user/list/$',views.userList, name='user_list'),
    url(r'^user/list/(.+)/$',views.userList,name='user_listcc'),
    url(r'^user/$',views.userList),
    url(r'^user/add/$',views.userAdd),
    url(r'^user/alter/(.+)/$',views.userAlter,name='user_alter'),
    # url(r'^user/alter/(?P<id>\d+)/$', UserInfoUpdate.userAlter,name='user_alter'),
    # url(r'^user/alter/(.+)/$', UserInfoUpdate.userAlter,name='user_alter'),
    url(r'^cmdb/serverlist/$',views.serverList, name='server_list'),
    url(r'^cmdb/serverlist/(.+)/$',views.serverList,name='server_listcc'),
    url(r'^cmdb/serveradd/$',views.serverAdd, name='server_add'),
    url(r'^cmdb/hostadmin/$',views.hostAdmin, name='hostadmin'),
    url(r'^cmdb/monitor/$',views.getMonitor, name='monitor'),
    url(r'^cmdb/$',views.serverList),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': DjangoWeb.settings.STATIC_ROOT }),
]

