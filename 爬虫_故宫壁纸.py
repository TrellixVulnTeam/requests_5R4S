import re
import requests as req
import os


if __name__ == '__main__':

    url='https://www.dpm.org.cn/lights/royal.html'
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

    if not os.path.exists('./gugong'):
        os.mkdir('./gugong')

    '''<img alt="元 赵雍挟弹游骑图轴（局部）" title="元 赵雍挟弹游骑图轴（局部）" src="https://img.dpm.org.cn/Uploads/Picture/2020/12/29/s5feaddb7e9954.jpg">'''
    for i in range(60,110):        #爬取110页
        url='https://www.dpm.org.cn/lights/royal/p/'+str(i)+'.html'
        try:
            response=req.get(url=url,headers=headers).text
            rex=r'<img alt=.*?src="(.*?\.jpg)">'    #（）只返回（）里匹配的内容列表
            imgurllist=re.findall(rex,response,re.S)   #将每页中包含的图片地址存起来。  re.S ：表示在同行匹配  re.M ：多行匹配
            for src in imgurllist:
                imgdata=req.get(src).content     #下载每一涨图片
                imgname='./gugong/'+str(src).split('/')[-1]
                with open(imgname,'wb') as fw:
                    fw.write(imgdata)
                    print(str(src).split('/')[-1],'下载成功！！！')
        except BaseException as be:
            print(be)
            continue
