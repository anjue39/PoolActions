# 这是未使用request组件的代码
# 代码适用于遍历某网址目录文件夹下，找到文件名含有当前日期的订阅文件并收集它

import urllib.request
import yaml
import re
import ssl
import os
import time
from datetime import datetime, timedelta, timezone

# 忽略SSL证书验证
ssl._create_default_https_context = ssl._create_unverified_context

def fetch(proxy_list):
    # 获取当前日期
    current_date = time.strftime("%Y%m%d", time.localtime())
    # 数据源的基础URL
    baseurl = 'https://raw.githubusercontent.com/anjue39/PoolActions/main/subscribe/'

    try:
        # 创建请求对象并添加头部信息
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        req = urllib.request.Request(baseurl, headers=headers)
        # 发送HTTP GET请求获取数据源页面
        with urllib.request.urlopen(req, context=ssl._create_unverified_context()) as response:
            if response.getcode() == 200:
                # 获取数据源页面的内容
                data = response.read()
                # 从页面内容中提取所有的文件名（带日期）
                filenames = re.findall(r'\d+', data.decode('utf-8'))
                for filename in filenames:
                    # 查找包含当前日期的文件名
                    if current_date in filename:
                        # 构造完整的URL
                        url = baseurl + filename
                        # 创建请求对象并添加头部信息
                        req = urllib.request.Request(url, headers=headers)
                        # 从URL获取数据并解析为YAML格式
                        with urllib.request.urlopen(req, context=ssl._create_unverified_context()) as yaml_response:
                            working = yaml.safe_load(yaml_response)
                            data_out = []
                            for x in working['proxies']:
                                data_out.append(x)
                            # 将解析的代理数据添加到列表中
                            proxy_list.append(data_out)
                            print("Data fetched successfully.")
                            return
            print("File not found for the current date.")
    except urllib.error.URLError as e:
        print(f"Error fetching data: {str(e)}")

# 创建一个空的代理列表
proxy_list = []
# 调用fetch函数，将获取的代理数据填充到列表中
fetch(proxy_list)

# 指定保存文件的目录
dirs = './subscribe'
if not os.path.exists(dirs):
    os.makedirs(dirs)

# 获取当前时间并格式化为字符串
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
time_str = utc_dt.astimezone(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M')

# 拼接保存文件的完整路径
filename = dirs + '/clash5.yaml'
# 打开文件并写入代理数据
with open(filename, 'w+', encoding='utf-8') as f:
    # 添加文件的头部信息
    info ='#' + time_str + ' 更新\n' + '#本yaml文件由Actions定时生成\n#项目地址：'
    f.write(info)
    # 使用yaml.safe_dump将代理列表以YAML格式写入文件
    yaml.safe_dump(data_out, f, default_flow_style=False)
