# 商城项目：

## 项目背景：

​		自己做的一个商城项目（感觉商城项目挺火的所以做了），没有抄黑马的那个美多商城，也算是在普通商城的基础上改进的，毕竟商城系统几乎都一个样。

## 项目技术：

​		项目最早使用了**python3.10、django 4.2、DRF（Django REST framework）,MySQL**实现,后续添加了**Redis，simpleJWT，celery**异步任务，定时任务，用**RabbitMQ**做的**celery**的消息代理，二次封装了阿里云短信的SDK，同时添加了**商品推荐**（简单手搓了一个**MapReduce**给收藏的商品进行排序，然后推荐同类商品，因为是自己做的项目，没啥数据训练模型就不用机器学习实现了），添加了**以图搜图**的功能（感觉挺好实现的功能，不知道为啥网上大部分的商城项目都没有这个功能，图片相似度对比，设置阈值进行返回给用户），给celery定时任务设置了一个执行完毕后将执行结果发送给管理员的功能（刚好学到就把功能加上了）。

## 主要功能：

​	**用户**：用户登录注册，个人信息修改，头像上传，设置默认收货地址，发送短信验证码，绑定手机号，解绑手机号，刷新token，校验token。

​	**地址**：增删改查。

​	**历史记录**：创建。

​	**商品**：获取商品列表（搭配filter进行筛选），获取商城主页，获取单个商品，收藏商品，获取收藏的商品列表，取消收藏，获取商品分类信息。

​	**购物车**：添加商品到购物车，查看购物车列表，修改购物车商品状态（是否选中），修改购物车商品数量。

​	**订单**：创建订单， 获取订单列表，订单状态切换。

## 部署流程：

### MySQL：

要求**8.0**以上版本，低版本会报错。

详细安装教程自己搜。

终端链接数据库

your_username为你的用户名

```shell
mysql -u your_username -p
```

输入密码进入数据库

```sql
create database shop;
```

返回OK创建成功

### Redis：

**GitHub**上安装，官方没有**Windows**版。

详细安装教程自己搜，应该没有版本问题，如果有可以联系我。

### RabbitMQ：

因为**Celery**用**RabbitMQ**做的消息代理，所以要下载一个**RabbitMQ**，如果不用**RabbitMQ**做消息代理的话可以不安装的，settings.py中代码都写好了可以切换消息代理和任务存储位置等，请根据自己需求选择。

安装**RabbitMQ**前，要安装**Erlang**，详细见**RabbitMQ**官方文档

详细安装教程自己搜，应该没有版本问题，如果有可以联系我。

### Python环境配置：

1.创建虚拟环境（以免包冲突之类的，最好还是建一个新的虚拟环境）

以conda为例，在conda命令行输入

```shell
conda create -n env_name python=3.10
```

安装配置项（建议用清华源，目前还能用）

```shell
pip install -r requirements.txt
```

打开settings.py文件，配置数据库等信息，（用户名，密码等换成自己的）

生成数据库迁移文件

```shell
python manage.py makemigrations
```

数据迁移

```shell
python manage.py migrate
```

启动celery异步任务

```shell
celery -A shop worker -l debug -P eventlet
```

启动celery定时任务

```shell
celery -A shop beat --loglevel=info
```

启动celery日志（flower）

如果Rabbit做消息代理的话就打开RabbitMQ的那个作业网址

```shell
celery -A shop flower
```

项目启动

终端输入

```shell
python manage.py runserver
```

嫌麻烦就在编辑一个形参运行

![](D:\桌面\Snipaste_2024-06-25_20-16-57.jpg)

![Snipaste_2024-06-25_20-17-20](D:\桌面\Snipaste_2024-06-25_20-17-20.jpg)

8000为端口号

项目没有前段部分，但是有接口测试文档，有想做前端的小伙伴可以直接push上来哦



## 项目结构

├─cart			购物车模块
│  │  admin.py			(admin后台)
│  │  apps.py
│  │  models.py			(数据库模型)
│  │  permissions.py	(权限管理)
│  │  serializers.py		(序列化器)
│  │  tests.py
│  │  urls.py				(路由)
│  │  views.py			(视图)
│  │  __init__.py
│  │ 
│  │
├─common		通用工具
│  │  aliyun_message.py		(阿里云短信封装)
│  │  authenticate.py				(身份认证)
│  │  db.py							(抽象模型类)
│  │  map_reduce.py			(MapReduce,商品用的)
│  │  recommend.py				(商品推荐,废弃)
│  │  __init__.py
│  │
│  │
├─file				媒体文件
│  └─image
│          banana.jpg
│          beef.jpg
│          carrots.jpg
│          chicken.jpg
│          frunt.jpg
│          meet.jpg
│          posters1.jpg
│          posters2.jpg
│          posters3.jpg
│          vegetables.jpg
│          头像.jpg
│
├─goods			商品模块
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  permissions.py
│  │  serializers.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │
├─history			历史记录模块
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  serializers.py
│  │  tests.py
│  │  views.py
│  │  __init__.py
│  │
├─order			订单模块
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  serializers.py
│  │  tasks.py			(异步任务和定时任务)
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
├─shop			项目配置模块
│  │  asgi.py
│  │  celery.py		(celery任务配置)
│  │  enums.py
│  │  settings.py
│  │  urls.py
│  │  wsgi.py
│  │  __init__.py
├─templates		模版（没啥用）
├─users				用户模块
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  permissions.py
│  │  serializers.py
│  │  tasks.py
│  │  urls.py
│  │  views.py
│  │  __init__.py



## 联系方式：

​	QQ：1071519731

​	微信：17692275126

​	手机号：17692275126

​	谷歌邮箱：liuzepu1016@gmail.com

​	QQ邮箱：1071519731@qq.com