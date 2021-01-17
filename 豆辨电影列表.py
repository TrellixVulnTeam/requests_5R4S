import requests as req
import urllib.parse
import json
import time
from random import *
import urllib.request as rqs
import re

from urllib3 import HTTPConnectionPool


def getproxy(url):

    context=req.get(url).text
    ip=''
    #print(context)
    #context=response.read().decode('utf-8')
    #要匹配的格式如下，且有换行符
    '''<td>18</td>
    <td>111.11.227.114</td>
    <td>80</td>'''
    #p=r'(?:(?:[0,1]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:[0,1]?\d\d|2[0-4]\d|25[0-5])' #匹配IP地址
    pattern = re.compile(r'((?:(?:[0,1]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:[0,1]?\d\d|2[0-4]\d|25[0-5]).*<th>(?:\d{1,5}))</th>',re.S)
    ips=re.findall(pattern,context)
    proxyurls = {}
    #print('ips',ips)
    for tempip in ips:
        #print(tempip)
        ip1=str(tempip).replace('</th>\r\n',':',-1).replace('\ ','',-1).replace(' ','',-1).replace('</tr><tr>','',-1).replace('<th>','',-1)
        ip2=ip1.split('\r\n',-1)  # ip2 :['140.255.45.68:29684:山东省济南市电信:高匿:', '123.73.82.159:32221:山西省晋中市中移铁通:高匿:', '123.73.63.39:32221:山西省运城市中移铁通:高匿:', '110.246.205.183:22265:河北省邢台市联通:高匿:', '183.2.101.72:18483']
        for tmepip2 in ip2:

            #print(tmepip2)
            #print(ip2)
            #print('ip1 ',ip1)
            tip=tmepip2.split(':')
            #print('tip:',tip)
            ip2,port='http:'+'http://'+tip[0],tip[1]
            ip=tip[0]+":"+tip[1]
            return ip
            #proxyurls[ip]=port
            #print(proxyurls)
    #print(proxyurls)
    #proxy=choice(proxyurls)
    #print(proxy)
    return ip
#使用代理

def list_json(response,start):
    data=response.json()
    #print(data)
    if 'msg' in data:
        print('请求过于频繁')
        exit(0)
    datalist=data['data']
    j=start
    for text in datalist:
        j+=1
        title=text['title']
        rate=text['rate']
        casts=text['casts']
        directors=text['directors']
        print('第%d部电影:名称：%s 评分：%s 演员：%s'%(j,title,rate,casts))
        #print(data['data']['title'],data['data']['rate'],data['data']['directors'])

if __name__ == '__main__':

    url='https://movie.douban.com/j/new_search_subjects'
    for start in range(0,1000,10):
        params={
            'sort': 'U',
            'range': '0, 10',
            'tags':'',
            'start': start
        }
        proxy=getproxy(url='http://http.zhiliandaili.cn/')

        proxies = {"http": "http://"+proxy }
        print("代理地址为：",proxies)
        headers1 = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Mobile Safari/537.36'}
        headers2 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        rand=randint(1,2)
        try:
            if rand==1:
                response=req.get(url=url,params=params,headers=headers1,proxies=proxies)
                print(response.url)
            else:
                response = req.get(url=url, params=params, headers=headers2,proxies=proxies)

            list_json(response,start)
            if start % 50 == 0:
                time.sleep(10)
        except urllib.error.URLError as urler:
            print('地址错误', urler)
        except urllib.error.ContentTooShortError as cr:
            print('连接错误', cr)
            if rand == 1:
                response = req.get(url=url, params=params, headers=headers1, proxies=proxies)
            else:
                response = req.get(url=url, params=params, headers=headers2, proxies=proxies)
            list_json(response, start)
            if start%50==0:
                time.sleep(10)
        except urllib.error.HTTPError as httper:
            print('访问出现错误，尝试中...')
            if rand == 1:
                response = req.get(url=url, params=params, headers=headers1, proxies=proxies)
            else:
                response = req.get(url=url, params=params, headers=headers2, proxies=proxies)
            list_json(response, start)
            #time.sleep(1 / 10)