import urllib.request
import requests
import yaml
import re
import ssl
import os
import time
from datetime import datetime, timedelta, timezone

def fetch(proxy_list):
    current_date = time.strftime("%Y%m%d", time.localtime())
    baseurl = 'https://raw.githubusercontent.com/guoxing123/jiedian/main'

    try:
        response = requests.get(baseurl, timeout=240)
        if response.status_code == 200:
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
        else:
            print("Error fetching data. Response status:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", str(e))

# Create the 'subscribe' directory if it doesn't exist
dirs = './subscribe'
if not os.path.exists(dirs):
    os.makedirs(dirs)

# Fetch the proxy data
proxy_list = []
fetch(proxy_list)

# Generate the timestamp
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
time_str = utc_dt.astimezone(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M')

# Write the data to the file
filename = os.path.join(dirs, 'clash5.yaml')
with open(filename, 'w', encoding='utf-8') as f:
    info = f"# {time_str} 更新\n" \
           f"# 本yaml文件由Actions定时生成\n" \
           f"# 项目地址：https://github.com/xhrzg2017/ProxiesActions\n"
    f.write(info)
    for proxy_data in proxy_list:
        f.write(proxy_data)
        f.write('\n')

print("Data saved successfully.")
