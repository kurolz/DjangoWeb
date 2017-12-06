#！python3
import datetime,json
import urllib.request, urllib.parse, urllib.request
import pymysql.cursors

def collect():
    memorytotal_now = ''
    memoryavai_now = ''
    zabbix_host_info = dataHandle(func=getZabbixHost)
    for i in zabbix_host_info:
        '''获取空闲内存'''
        memoryavai_dict = dataHandle(func=getmemoryavai, hostid=i['hostid'])
        '''获取总内存'''
        memorytotal_dict = dataHandle(func=getmemorytotal, hostid=i['hostid'])
        for i in memoryavai_dict:
            memoryavai_now = i['prevvalue']  # 获取空闲内存
        for i in memorytotal_dict:
            memorytotal_now = i['prevvalue']  # 获取总内存
        '''内存使用率'''
        memory_useratio = (int(memorytotal_now) - int(memoryavai_now)) / int(memorytotal_now)

        '''写入数据库'''
        # 连接数据库
        db = pymysql.Connect(host="localhost", user="root", passwd="******", db="OBServer", charset="utf8")
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # SQL 语句
        sql = "insert into webserver_monitormemory(avai,total,ratio,time,hostid) values('%s','%s','%.4f','%s',%d)"
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hostid = int(i['hostid'])
        data = (memoryavai_now, memorytotal_now, memory_useratio,dt,hostid)
        cursor.execute(sql % data)
        db.commit()
        # 关闭数据库连接
        db.close()

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

def getmemoryavai(*args, **b):
    '''
    获取空闲内存
    '''
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": "extend",
            "hostids": b["parameter"],
            "search": {
                "key_": "vm.memory.size[available]"
            }
        },
        "auth": b["session"],
        "id": 2
    })
    return data

def getmemorytotal(*args, **b):
    '''
    获取总内存
    '''
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": "extend",
            "hostids": b["parameter"],
            "search": {
                "key_": "vm.memory.size[total]"
            }
        },
        "auth": b["session"],
        "id": 2
    })
    return data

def timerFun(sched_Timer):
    flag=0
    while True:
        now=datetime.datetime.now()
        if now==sched_Timer:
            collect()
            flag=1
        else:
            if flag==1:
                sched_Timer=sched_Timer+datetime.timedelta(minutes=1)
                flag=0

if __name__ == '__main__':
    collect()