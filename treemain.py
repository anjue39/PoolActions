
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

#6.保存到文件中
print("保存到文件中")
dirs = './subscribe'
with open(dirs+'/clash5.yaml', 'w+', encoding='utf-8') as f:
    # print(data)
    info ='#'+time+'更新 \n' + '#本yaml文件由Actions定时生成\n#项目地址：https://github.com/xhrzg2017/ProxiesActions\n'
    f.write(info)
    f.close()
with open(dirs + '/clash5.yaml', 'ab') as f:
    f.write(data)
