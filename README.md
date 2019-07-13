# mmscrapy
scrapy框架搭建的爬虫项目，在这个项目里面有自己创建的spider。

## mmscrapy爬虫程序


## 项目爬虫创建
``` 
scrapy startproject project
```
## 爬虫执行
```
scrapy crawl novel_spider -o novel.csv

```

## scrapyd 爬虫管理工具
scrapyd是一款对scrapy爬虫进行页面管理的工具，可以将scrapy爬虫打包添加到scrapyd进行爬虫。
### 1、scrapyd安装
``` 
pip install scrapyd

```

### 2、scrapyd-client安装

``` 
pip install scrapyd-client

```

安装scrapyd-client可以使用scrapyd-deploy将scrapy的包上传到scrapyd。在window中会出现
scrapyd-deploy命令不存在的问题，需要在python的Scripts中添加scrapyd-deploy.cmd脚本。
``` 
@echo off
"D:\Program Files"\python2.7.15\python "D:\Program Files"\python2.7.15\Scripts\scrapyd-deploy %*
```

### 3、scrapyd-deploy部署

#### 3.1、启动scrapyd
``` 
scrapyd
```

#### 3.2、添加setup.py打包脚本
``` 
from setuptools import setup, find_packages

setup(
    name='mmscrapy',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = mmscrapy.settings']}
)
```

#### 3.3、使用scrapyd-deploy进行打包
``` 
scrapyd-deploy.cmd --build-egg mmscrapy.egg
```

#### 3.4、将egg包添加到scrapyd中
``` 
scrapyd-deploy.cmd -a -p mmscrapy
```

### 4、scrapyd脚本执行
``` 
curl http://localhost:6800/schedule.json -d project=mmscrapy -d spider=novel_spider
```

## SpiderKeeper爬虫监控
SpiderKeeper是对运行在scrapyd里面的爬虫程序进行监控和管理，方便用户操作。可以创建一次任务
和定时性任务。

### 1、SpiderKeeper安装
``` 
pip install spiderkeeper
pip install scrapy_redis
```

### 2、SpiderKeeper运行
进入到python的Scripts目录下 直接运行spiderkeeper
``` 
spiderkeeper
```

### 3、SpiderKeeper项目运行
- 页面直接创建项目,项目名称根据业务来创建
- 上传egg文件(scrapyd-deploy --build-egg output.egg)
- 文件上传完成之后可以在spider-Dashborad里面查看spider
- 选择在jobs的Dashborad和Periodic里面添加job

