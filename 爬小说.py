import  requests as req
import bs4

def get_urllist():
    list=[]
    url='https://www.shicimingju.com/book/'
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    urllist=[]
    urles=req.get(url=url,headers=headers).content.decode('utf-8')
    url_bs=bs4.BeautifulSoup(urles,'lxml')
    urllsit=url_bs.select('.booknark_card ul>li>a')
    for urla in urllsit:
        #print(urla)
        urltext='https://www.shicimingju.com'+urla['href']
        titletext=urla.text
        list.append(titletext+'|'+urltext)

    return list

def getxiaoshuo(url1,bookname):
    url=url1
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    response=req.get(url=url,headers=headers).content.decode('utf-8')
    #print(response.content.decode('utf-8'))
    title_bs=bs4.BeautifulSoup(response,'lxml')
    title_list=title_bs.select('.book-mulu>ul>li')
    #print(title_list)
    fw=open(bookname+'.txt','w',encoding='utf-8')
    for text in title_list:
        try:
            title=text.a.string
            detail_url='https://www.shicimingju.com'+text.a['href']
            detail_text=req.get(url=detail_url,headers=headers).content.decode('utf-8')
            detail_bs=bs4.BeautifulSoup(detail_text,'lxml')
            context=detail_bs.find('div',class_='chapter_content').text
            fw.write(title+'\n'+context+'\n')
            print(title+': 爬取成功！')
        except BaseException as BE:
            print(BE)
            continue
    fw.close()

if __name__ == '__main__':
    #getshuihuzhuan()
    list=get_urllist()
    for url1 in list:
        url=url1.split('|')[-1]
        bookname=url1.split('|')[0]
        getxiaoshuo(url,bookname)