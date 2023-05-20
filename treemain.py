import time
import requests
import yaml

def fetch(proxy_list):
    current_date = time.strftime("%Y%m%d", time.localtime())
    baseurl = 'https://github.com/guoxing123/jiedian/raw/main/'
    
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
proxy_list = []
fetch(proxy_list)

# 保存结果到文件
filename = './subscribe'
with open(filename, 'w') as file:
    for proxies in proxy_list:
        for proxy in proxies:
            file.write(proxy + '\n')
print(f"Results saved to '{filename}'")
