# DjangoWeb
Background based on Django！
因为我还是学生，无法得到实际需求，所以这个项目只有用户管理功能，项目暂停，工作以后会继续完善。为此将会重新开发一个博客网站项目继续学习。

@@ 使用Docker-compose部署Django环境：
@@ System - Centos7.0
@@ Django - 1.9.5
@@ Python - 3.6.0

yum -y install docker

systemctl start docker

###使用daocloud镜像加速###
vim /etc/docker/daemon.json
{
    "registry-mirrors": [
        "http://5c51d642.m.daocloud.io"
    ],
    "insecure-registries": []
}

docker pull mysql   # 下载镜像到本地

docker pull django:1.9.5  # 下载镜像到本地

docker pull python:3.6.0   # 下载镜像到本地

mkdir /mysite

mkdir /mysite/DjangoWeb

mkdir /mysite/db


vim /mysite/Dockerfile

Dockerfile包含创建镜像所需要的全部指令。在项目根目录下创建Dockerfile文件，其内容如下：

FROM python:3.6.0
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
RUN mkdir /code/db
WORKDIR /code
ADD ./DjangoWeb/requirements.txt /code/
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt 
ADD . /code/

第1行的FROM指令表示新的镜像将基于python:2.7的镜像来构建 
第2行的ENV为环境变量（PYTHONUNBUFFERED见这里） 
第3行的RUN指令表示在镜像内新建/code目录 
第4行指定指定RUN、CMD与ENTRYPOINT命令的工作目录 
第5行是将./mysite/requirements.txt文件添加到刚才新建的code目录中 
第6行运行pip安装所需的软件

vim /mysite/docker-compose.yml

之前的Dockerfile定义了一个应用，而使用compose，可以在一个文件里，定义多容器的应用。该YAML配置语言，用于描述和组装多容器的分布式应用。在项目根目录创建docker-compose.yml文件，其内容如下：

db:
  image: mysql
  expose:
    - "3306"
  volumes:
    - ./db:/var/lib/mysql
  environment:
    - MYSQL_DATABASE=mysitedb
    - MYSQL_ROOT_PASSWORD=888888

web:
  build: .
  command: python ./DjangoWeb/manage.py runserver 0.0.0.0:8000
  volumes:
    - .:/code
  ports:
    - "8000:8000"
  links:
    - db

db标签： 
images表示使用mysql镜像 
expose表示暴露端口3306，但不发布到宿主机上 
volume表示挂载宿主机的路径作为卷，冒号左边为宿主机路径，右边为镜像内路径 
environment为环境变量，每个容器都有自己定义的环境变量，具体查看镜像手册中的mysql

web标签： 
build指定建立Dockerfile路径 
command将覆盖默认的命令 
ports指定主机开放的端口 
links指向其他容器中的服务

vim /mysite/DjangoWeb/requirements.txt 

在子目录mysite下requirements.txt文件，该文件内容如下:
django==1.9.5
mysqlclient
django-admin-bootstrapped
bootstrap3
pillow


构建镜像:
cd /mysite

docker-compose build

docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
mysite_web          latest              43b4615f87c7        6 minutes ago       720.5 MB
docker.io/mysql     latest              b4e78b89bcf3        9 days ago          412.3 MB
docker.io/python    3.6.0               a1782fa44ef7        7 months ago        687.1 MB
docker.io/django    1.9.5               c5b6e7c5c44c        17 months ago       433.4 MB


docker-compose run web django-admin.py startproject webserver ./DjangoWeb

docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                     PORTS               NAMES
ad0c75e2fd3d        mysite_web          "django-admin.py star"   5 minutes ago       Exited (0) 5 minutes ago                       mysite_web_run_1
77e91e05178d        mysql               "docker-entrypoint.sh"   5 minutes ago       Up 5 minutes               3306/tcp            mysite_db_1

chmod -R 777 DjangoWeb

vim DjangoWeb/webserver/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysitedb',
        'USER': 'root',
        'PASSWORD': '888888',
        'HOST': 'db',
        'PORT': 3306,
    }
}

添加net端口映射
[root@VM_34_67_centos DjangoWeb]# docker inspect 1bf8642343e3 | grep IPAddress
            "SecondaryIPAddresses": null,
            "IPAddress": "172.17.0.3",
                    "IPAddress": "172.17.0.3",
[root@VM_34_67_centos DjangoWeb]# iptables -t nat -A  DOCKER -p tcp --dport 80 -j DNAT --to-destination 172.17.0.3:8000     


导入数据库。

############## 先前台运行无报错再转入后台运行 ##############
进入mysite目录，启动容器：
docker-compose up
退出应用Crtl+C

后台运行：
docker-compose up -d

退出应用：
docker-compose stop

注意down会删除容器。






