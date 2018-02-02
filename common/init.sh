#!/usr/bin/env bash

# docker 查询mongo的image
docker search mongo

# docker下载mongo的image
docker pull mongo

# docker运行mongo容器
docker run -p 127.0.0.1:27017:27017 -d -v /data/db:/data/db --name mongodb mongo --storageEngine wiredTiger

# redis 相关
docker search redis
docker pull redis
docker run -p 127.0.0.1:6379:6379 --name redis redis