import requests as req
from multiprocessing import Pool
from lxml import  etree
import re

def geturl():
    url='http://www.sharenice.net/t-6Z+z5LmQ'
    headers={}
    page_text=req.get(url=url,headers=headers).text
    tree=etree.HTML(page_text)
    li_list=tree.xpath('//div[@class="cate-block first-block"]//ul/li')
    #print(li_list)
    video_urls=[]
    for li in li_list:
        try:
            #print(li)
            detial_url=''+li.xpath('./span[@class="cover"]/a/@href')[0]
            #print(detial_url)
            detial_title=li.xpath('./span[@class="cover"]/a/@title')[0]+'.mp4'
            #print(detial_title,detial_url)
            #print(detial_url)
            detial_page_text=req.get(url=detial_url,headers=headers).text
            #print(detial_page_text)
            '''src = "https://video.pearvideo.com/mp4/adshort/20210125/cont-1717851-15586820_adpkg-ad_hd.mp4"'''
            regex='src="(https.*?\.mp4)'
            video_url=re.findall(regex,detial_page_text)[0]
            if video_url=='':
                continue
            #print(video_url)
            dict1= {'name':detial_title,'url':video_url}
            video_urls.append(dict1)
        except BaseException as BE:
            continue
    #print(video_urls)
    return video_urls

def save_video(reponse,name):
    with open(name,'wb') as fw:
        fw.write(reponse)
    fw.close()
    print('%s /保存成功！！' %name)

def getvideo(video_urls):

    #name=li['name']
    url1=video_urls['url']
    #print(url)
    context=req.get(url=url1).content
    print('正在保存：%s' %video_urls['name'])
    #save_video(context,name)
    with open(video_urls['name'], 'wb') as fw:
        fw.write(context)
    fw.close()
    print('%s /保存成功！！' % video_urls['name'])

if __name__ == '__main__':
    videourls=geturl()
    #print(videourls)
    #开启8线程
    pool=Pool(8)
    pool.map(getvideo,videourls)  #传入一个方法和一个可迭代的对象
    pool.close()
    pool.join()

