#!/bin/bash
# 这里使用的是 main 分支，根据需求自行修改
git pull origin main && git add && git commit -m "$(date '+%Y.%m.%d %H:%M:%S') 订阅更新" && git push origin main

