#!/usr/bin/env bash

# docker下载mongo的image
docker pull mongo

# docker运行mongo容器
docker run -p 27017:27017 -d -v /data/db:/data/db --name mongodb mongo --storageEngine wiredTiger

#