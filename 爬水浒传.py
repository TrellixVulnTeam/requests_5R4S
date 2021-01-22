import  requests as req
import bs4

def getshuihuzhuan():
    url='https://www.shicimingju.com/book/hongloumeng.html'
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    response=req.get(url=url,headers=headers).content.decode('utf-8')
    #print(response.content.decode('utf-8'))
    title_bs=bs4.BeautifulSoup(response,'lxml')
    title_list=title_bs.select('.book-mulu>ul>li')
    #print(title_list)
    fw=open('./shuihuzhuan.txt','w',encoding='utf-8')
    for text in title_list:
        title=text.a.string
        detail_url='https://www.shicimingju.com'+text.a['href']
        detail_text=req.get(url=detail_url,headers=headers).text
        detail_bs=bs4.BeautifulSoup(detail_text,'lxml')
        context=detail_bs.find('div',class_='chapter_content').text
        fw.write(title+'\n'+context+'\n')
        print(title+': 爬取成功！')
    fw.close()

if __name__ == '__main__':
    getshuihuzhuan()