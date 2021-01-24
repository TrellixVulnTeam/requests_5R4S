from lxml import etree
import requests as req

def getnewhourse():
    url = 'https://cs.fang.ke.com/loupan/pg{0}'
    luopaninfo=[]
    for i in range(1,100):
        url1=url.format(i)
        #print(url1)
        header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
        response=req.get(url=url1,headers=header).text
        tree=etree.HTML(response)
        li_list=tree.xpath('//div[@class="resblock-list-container clearfix"]/ul[@class="resblock-list-wrapper"]/li') #//：任意层级 @class="resblock-list-container clearfix"
        #print(li_list)
        luopandata=[]
        for li in li_list:
            title=li.xpath('.//div[@class="resblock-desc-wrapper"]/div[@class="resblock-name"]/a/text()')[0]   #.:从当前标签下开始，//：任意层级 @class="resblock-desc-wrapper"：通过属性值定位 ，text() 取值
            print('楼盘：'+title) #楼盘名称

            li_locale=li.xpath('.//div[@class="resblock-desc-wrapper"]/a[@class="resblock-location"]/@title')[0]
            print('位置：'+li_locale) #楼盘位置
            price=li.xpath('.//div[@class="resblock-price"]//span[@class="number"]/text()')[0]
            print('均价：'+price) #均价
            try:
                total_price = li.xpath('.//div[@class="resblock-price"]//div[@class="second"]/text()')[0]
                #print(total_price)  # 总价
            except BaseException :
                total_price = '待定'
            print('总价:'+total_price)  # 总价
            li_url = 'https://cs.fang.ke.com' + \
                     li.xpath('.//div[@class="resblock-desc-wrapper"]/div[@class="resblock-name"]/a/@href')[
                         0]  # @href:取属性的名称
            print('详情：'+li_url+'\n')  # 楼盘链接
            luopandata.append([title,li_locale,price,total_price,li_url])
        luopaninfo.append(luopandata)
    print(luopaninfo)
    with open('./贝壳找房—新房.txt','w',encoding='utf-8')  as fw:
        fw.write(str(luopaninfo))
        #print(luopandata)

if __name__ == '__main__':
    getnewhourse()
