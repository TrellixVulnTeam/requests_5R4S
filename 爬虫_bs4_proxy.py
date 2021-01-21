import bs4
import lxml
import requests  as req
from random import *

def get_proxy():
    url = 'https://ip.jiangxianli.com/?page=1'  # 提供代理IP的页面
    headers = {
        'Cookie': 'UM_distinctid=1770efbd8b55c-08e67b79499c89-303464-144000-1770efbd8b676; Hm_lvt_b72418f3b1d81bbcf8f99e6eb5d4e0c3=1610864122; CNZZDATA1278691459=828572365-1610863866-https%253A%252F%252Fwww.google.com%252F%7C1611145428; Hm_lpvt_b72418f3b1d81bbcf8f99e6eb5d4e0c3=1611150489',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    response = req.get(url=url, headers=headers)
    '''</li>
</ul>
</div>
<div class="layui-row">
    <div class="layui-col-md9 ip-tables">
        <div class="layui-form">
            <table class="layui-table">
                <thead>
                    <tr>
                        <th>IP</th>
                        <th>端口</th>
                        <th>匿名度</th>
                        <th>类型</th>
                        <th width=160>位置</th>
                        <th>所属地区</th>
                        <th>运营商</th>
                        <th>响应速度</th>
                        <th>存活时间</th>
                        <th>最后验证时间</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>88.198.50.103</td>
                        <td>8080</td>
                        <td>透明</td>
                        <td>HTTP</td>
                        <td>德国 Sachsen XX</td>
                        <td>德国</td>
                        <td>XX</td>
                        <td>3.004秒</td>
                        <td>13小时22分钟</td>
                        <td>2021-01-20 21:50:46</td>
                        <td>
                            <button class="layui-btn layui-btn-sm btn-copy" data-url="http://88.198.50.103:8080" data-unique-id="3f799c4587b317c3af1e77aa7876de1e">复制</button>
                            <button class="layui-btn layui-btn-sm btn-speed " data-url="http://88.198.50.103:8080" data-protocol="http" data-ip="88.198.50.103" data-port="8080" data-unique-id="3f799c4587b317c3af1e77aa7876de1e">测速</button>
                        </td>
                    </tr>
                    <tr>
                        <td>110.243.9.34</td>
                        <td>9999</td>
                        <td>高匿</td>
                        <td>HTTP</td>
                        <td>中国 河北 唐山</td>
                        <td>中国</td>
                        <td>联通</td>
                        <td>436毫秒</td>
                        <td>4分钟51秒</td>
                        <td>2021-01-20 21:50:46</td>
                        <td>
                            <button class="layui-btn layui-btn-sm btn-copy" data-url="http://110.243.9.34:9999" data-unique-id="d290939f25239d1cddd349012888111e">复制</button>
                            <button class="layui-btn layui-btn-sm btn-speed " data-url="http://110.243.9.34:9999" data-protocol="http" data-ip="110.243.9.34" data-port="9999" data-unique-id="d290939f25239d1cddd349012888111e">测速</button>
                        </td>
                    </tr>                    
                </tbody>
            </table>'''
    listhead = ['IP', '端口', '匿名度', '类型', '位置', '所属地区', '运营商', '响应速度', '存活时间', '最后验证时间']
    listbody = []
    tempbody = bs4.BeautifulSoup(response.text, 'lxml')
    # print(tempbody)
    context = tempbody.find('div', class_="layui-form").findChild('tbody').find_all('tr')
    # print(context)
    tempdict = {}
    for tempda in context:
        tdlist = tempda.find_all('td')
        '''IP', '端口', '匿名度', '类型', '位置', '所属地区', '运营商', '响应速度', '存活时间', '最后验证时间'''
        ip1 = tdlist[0].text
        port1 = tdlist[1].text
        nmd1 = tdlist[2].text
        type1 = tdlist[3].text
        local1 = tdlist[4].text
        area1 = tdlist[5].text
        provider1 = tdlist[6].text
        speed1 = tdlist[7].text
        activetime1 = tdlist[8].text
        testtime1 = tdlist[9].text
        tempdict = {'ip': ip1, 'port': port1, 'nmd': nmd1, 'type': type1, 'local': local1, 'area': area1,
                    'provider': provider1, 'speed': speed1, 'activetime': activetime1, 'testtime': testtime1}
        listbody.append(tempdict)
    # print(listbody)

    chocieproxy= choice(listbody)
    proxy = {str(chocieproxy['type']).lower(): 'http://' + chocieproxy['ip'] + ':' + chocieproxy['port']}
    return proxy


if __name__ == '__main__':
    proxy=get_proxy()
    #print(proxy)
