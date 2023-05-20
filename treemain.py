import urllib.request
import requests
import yaml
import re
import ssl
import os
import time
from datetime import datetime, timedelta, timezone

# 忽略 SSL 验证
ssl._create_default_https_context = ssl._create_unverified_context

def fetch(proxy_list):
    current_date = time.strftime("%Y%m%d", time.localtime())
    baseurl = 'https://github.com/guoxing123/jiedian/raw/main/'

    try:
        response = requests.get(baseurl, timeout=240)
        if response.status_code == 200:
            data = response.content
            filenames = re.findall(r'\d+', response.text)
            for filename in filenames:
                if current_date in filename:
                    url = baseurl + filename
                    working = yaml.safe_load(requests.get(url, timeout=240).text)
                    data_out = []
                    for x in working['proxies']:
                        data_out.append(x)
                    proxy_list.append(data_out)
                    print("Data fetched successfully.")
                    return
        print("File not found for the current date.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {str(e)}")

# 添加请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

# 发送请求并读取数据
url = 'https://github.com/guoxing123/jiedian/raw/main/'
request = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(request, context=ssl._create_unverified_context())
data = response.read()

# 调用fetch函数
proxy_list = []
fetch(proxy_list)

dirs = './subscribe'
if not os.path.exists(dirs):
    os.makedirs(dirs)

utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
time_str = utc_dt.astimezone(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M')

with open(dirs+'/clash5.yaml', 'w+', encoding='utf-8') as f:
    info ='#'+time_str+'更新 \n' + '#本yaml文件由Actions定时生成\n#项目地址：https://github.com/xhrzg2017/ProxiesActions\n'
    f.write(info)

with open(dirs + '/clash5.yaml', 'ab') as f:
    f.write(data)
