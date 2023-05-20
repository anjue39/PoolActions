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

def fetch_and_save_data(baseurl, dirs, extension):
    # 获取当前日期
    current_date = time.strftime("%Y%m%d", time.localtime())

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
                data = response.read().decode('utf-8')
                # 从页面内容中提取所有的文件名（带日期）
                filenames = re.findall(r'\d+', data)
                for filename in filenames:
                    # 查找包含当前日期且具有指定扩展名的文件名
                    if current_date in filename and filename.endswith(extension):
                        # 构造完整的URL
                        url = baseurl + filename
                        # 创建请求对象并添加头部信息
                        req = urllib.request.Request(url, headers=headers)
                        # 从URL获取数据
                        with urllib.request.urlopen(req, context=ssl._create_unverified_context()) as yaml_response:
                            # 读取数据
                            data = yaml_response.read().decode('utf-8')
                            # 拼接保存文件的完整路径
                            filepath = os.path.join(dirs, f"{filename}.{extension}")
                            # 保存数据到文件
                            with open(filepath, 'w+', encoding='utf-8') as f:
                                f.write(data)
                            print(f"Data fetched and saved successfully: {filepath}")
                return
            print("File not found for the current date.")
    except urllib.error.URLError as e:
        print(f"Error fetching data: {str(e)}")


#3.构建请求对象
request = urllib.request.Request(url, headers=headers)  #使用Request可以加请求头对象
#4.发送请求对象
response = urllib.request.urlopen(request,context=context)
#5.读取数据
data = response.read()
#6.保存到文件中 验证数据
dirs = './subscribe'
if not os.path.exists(dirs):
    os.makedirs(dirs)
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
time = utc_dt.astimezone(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M')
with open(dirs+'/clash5.yaml', 'w+', encoding='utf-8') as f:
    # print(data)
    info ='#'+time+'更新 \n' + '#本txt文件由Actions定时生成\n#项目地址：https://github.com/xhrzg2017/ProxiesActions\n'
    f.write(info)
    f.close()
with open(dirs+'/clash5.yaml', 'ab') as f:
    f.write(data)
