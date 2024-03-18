# 异常检测项目更新

下载资源文件：
链接:https://pan.baidu.com/s/1C1aXEFtcQcunUWaiO-oH9Q  密码:3q1s

解压后：

```bash
.
├── dfa
│   └── resources

├── sex
│   └── resources

└── window
    └── resources
```

- 在 dfa_service/app/    下放入下载的dfa/resouces文件夹     
- 在 sex_service/app/    下放入下载的sex/resouces文件夹   
- 在 window_service/app/ 下放入下载的window/resouces文件夹   

比如
```
dfa_service
├── Dockerfile
├── app
│   ├── __init__.py
│   ├── __pycache__
│   ├── main.py
│   ├── model.py
│   ├── resources # 下载下来的文件夹
│   └── routers.py
├── log_conf.yaml
├── requirements-mac.txt
├── requirements.txt
└── service.log
```

> 为啥要有上面这一步？ 因为真的是穷的没存储

打镜像
```bash
docker-compose build
```

启动
```bash
docker-compose up -d
```

OpenAPI接口文档:     
`localhost:8004/docs`

注意： 不同客户要留3-5天，甚至更多的时间，对接别人的业务需求。