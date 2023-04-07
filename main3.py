import urllib.request
import ssl,os
context = ssl._create_unverified_context()

#1.数据url
url = 'https://sub.xeton.dev/sub?target=clash&url=https://link.jscdn.cn/1drv/aHR0cHM6Ly8xZHJ2Lm1zL3QvcyFBdTJrVnZsREc4MU1oZ0YtdkxLNG5ldkRuNWZ2P2U9cGJmZUFR&config=https://raw.githubusercontent.com/xhrzg2017/listes/main/Clash/Config/airport.ini&emoji=true&list=false&udp=false&tfo=false&scv=false&fdn=false&sort=false'
#2.添加请求头
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
#3.构建请求对象
print("构建请求对象")
request = urllib.request.Request(url, headers=headers)  #使用Request可以加请求头对象
#4.发送请求对象
print("发送请求对象")
response = urllib.request.urlopen(request,context=context)
#5.读取数据
print("读取数据")
data = response.read()
#print(data)
#6.保存到文件中
print("保存到文件中")
dirs = './subscribe'
if not os.path.exists(dirs):
    os.makedirs(dirs)
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
time = utc_dt.astimezone(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M')
with open(dirs+'/clash.yaml', 'w+', encoding='utf-8') as f:
    # print(data)
    info ='#'+time+'更新 \n' + '#本yaml文件由Actions定时生成\n#项目地址：https://github.com/xhrzg2017/ProxiesActions\n'
    f.write(info)
    f.close()
with open(dirs + '/clash.yaml', 'ab') as f:
    f.write(data)

#2.添加请求头
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
#3.构建请求对象
request = urllib.request.Request(url, headers=headers)  #使用Request可以加请求头对象
#4.发送请求对象
response = urllib.request.urlopen(request,context=context)
#5.读取数据
data = response.read()
#print(data)
#6.保存到文件中 验证数据
dirs = './subscribe'
if not os.path.exists(dirs):
    os.makedirs(dirs)
with open(dirs+'/clash3.yaml', 'wb') as f:
    f.write(data)
