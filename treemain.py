# 这是未使用request组件的代码
# 代码适用于遍历某网址目录文件夹下，找到文件名含有当前日期的订阅文件并收集它

import urllib.request
import ssl
import yaml
import re
import os
import time
from datetime import datetime, timedelta, timezone

# 忽略SSL证书验证
ssl._create_default_https_context = ssl._create_unverified_context

def fetch(proxy_list):
    current_date = time.strftime("%Y%m%d", time.localtime())
    baseurl = 'https://raw.githubusercontent.com/anjue39/PoolActions/main/subscribe/'

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        req = urllib.request.Request(baseurl, headers=headers)
        with urllib.request.urlopen(req, context=ssl._create_unverified_context()) as response:
            if response.getcode() == 200:
                data = response.read()
                filenames = re.findall(r'\d+', data.decode('utf-8'))
                for filename in filenames:
                    if current_date in filename:
                        if filename.endswith('.yaml'):
                            url = baseurl + filename  # 加上文件扩展名
                            req = urllib.request.Request(url, headers=headers)
                            with urllib.request.urlopen(req, context=ssl._create_unverified_context()) as yaml_response:
                                working = yaml.safe_load(yaml_response)
                                data_out = []
                                for x in working['proxies']:
                                    data_out.append(x)
                                proxy_list.append(data_out)
                                print("Data fetched successfully.")
                                return
            print("File not found for the current date.")
    except urllib.error.URLError as e:
        print(f"Error fetching data: {str(e)}")

proxy_list = []
fetch(proxy_list)

dirs = './subscribe'
if not os.path.exists(dirs):
    os.makedirs(dirs)

utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
time_str = utc_dt.astimezone(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M')

filename = dirs + '/clash5.yaml'
with open(filename, 'w+', encoding='utf-8') as f:
    info ='#' + time_str + ' 更新\n' + '#本yaml文件由Actions定时生成\n#项目地址：'
    f.write(info)
    yaml.safe_dump(proxy_list, f, default_flow_style=False)

