#!/bin/bash
status_log=$(git status -sb)
# 这里使用的是 main 分支，根据需求自行修改
  git status -s && git pull origin main && git add subscribe/clash.yaml && git commit -m "$(date '+%Y.%m.%d %H:%M:%S') 订阅更新" && git push origin main
