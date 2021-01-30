from selenium import webdriver
import time
from lxml import etree
#
def taobao_login():

    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])  #允许开发者模式

    wb=webdriver.Chrome(executable_path='../chromedriver.exe',options=chrome_option)
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
             'cookie': 'thw=cn; enc=k55ejDgCyYHPpb7u9M1dvzSYagIE4E3c6XKnZ3YO9AXob%2BLXYyG5WWn261L1ux78f2SRojEFixPKq%2F4qxsyfyA%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; cna=hPpNFx9XMAACAXjjJ1BrgNDK; tracknick=%5Cu4F4E%5Cu4EF7%5Cu5185%5Cu8D2D; t=2b3dcd1d57a868d66a1dbd8544ec431b; lgc=%5Cu4F4E%5Cu4EF7%5Cu5185%5Cu8D2D; uc3=id2=VvqjwRJH8ee3&vt3=F8dCuAFamaV%2FeKuLeyo%3D&lg2=W5iHLLyFOGW7aA%3D%3D&nk2=1oJt%2FeUUUJU%3D; sgcookie=E100f6H%2F6NfYVKeNdM8h06i1d8aap2qU4m7I7AiPCTZPzIu5KS%2FysuYwecr0bzoJtMm2H9GrBMbo23Chq6u7qne%2FTw%3D%3D; uc4=nk4=0%401DPkvxEhhrcjEyYA3PEpIox4uw%3D%3D&id4=0%40VHyuwQsF0iYF8PyKH3A7dwCmxY4%3D; _cc_=V32FPkk%2Fhw%3D%3D; mt=ci=-1_0; cookie2=1d914d9ab690b69596dda92d5cb50d02; _tb_token_=eb583e31e33d3; xlly_s=1; _m_h5_tk=4d82e6371749fa333bd66f4f4eb50fb0_1611917817702; _m_h5_tk_enc=83716a1456c1b32ae487b9aea8f98e8b; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=2DECED17E8A5BB43F30C99545FBE4048; uc1=cookie14=Uoe1g8CytIRcbQ%3D%3D; tfstk=cNUcBF9UroobfLmuAZgbTzjsmX1dZAjqhPzzzzEUMWAbLozPi_tyYXBPZxe0Wh1..; l=eBI5XIXRjjEF2L1kBO5CFurza779uIRbzsPzaNbMiInca6OCsFTq5NCInptp-dtjgtCbue-PmtmRRRe6Sszdg2HvCbH_7qCoWxJO.; isg=BMXFPnK1CVf9hy2Zpg7rRVFP1AH_gnkUHQZO8scqRfwLXufQjNGv5Dd8aIKoHpHM'}
    wb.get('https://login.taobao.com/')
    #模拟鼠标滚动一页
    wb.execute_script('window.scrollTo(0,document.body.scrollHeight)') #滚动一屏，加一些无相关的操作，模拟人工
    wb.execute_script('Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) ')  #将属性设置为非webdriver 方式，（淘宝针对这个有反爬机制）
    time.sleep(3)
    input_password=wb.find_element_by_xpath('//div[@class="input-plain-wrap input-wrap-password"]/input[@name="fm-login-password"]')
    input_password.send_keys('**********') #设置输入框值为‘
    time.sleep(3)
    input_user=wb.find_element_by_xpath('//div[@class="input-plain-wrap input-wrap-loginid "]/input[@name="fm-login-id"]')  #根据ID找到输入框
    input_user.send_keys('newhackerman@163.com')

    time.sleep(2)
    login_buttion=wb.find_element_by_xpath('//div[@class="fm-btn"]/button[@type="submit"]')  #找到‘搜索按钮’
    logpage=login_buttion.click() #
    return wb

def taobao_getdata(wb):
    #打开美妆页
    #wb.execute_script('Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) ')  #将属性设置为非webdriver 方式，（淘宝针对这个有反爬机制）
    wb.get('https://mei.taobao.com/')
    #对于没有id,name等属性值的iframe处理
    # element1 = wb.find_element_by_css_selector('# container > div > div.layui-tab-content > div.layui-tab-item.layui-show > iframe')
    # wb.switch_to.frame(element1)
    pagesource=wb.page_source
    #print(pagesource)
    tree=etree.HTML(pagesource)
    sorts=tree.xpath('//div[@class="col-sub J_Region"]//div[@class="ranking"]/li')
    products=[]
    print(sorts)
    for sort in sorts:
        print(sort)
        top=sort.xpath('./div[@class="pic"]/span[@class="top"]/@text()')[0] #排名
        text = sort.xpath('./div[@class="info"]/p[@class="text"]/@text()')[0] #名称
        cost=sort.xpath('./div[@class="info"]/p[@class="cost"]/span[@class="g_price g_price-highlight"]/strong/text()')[0] #价格
        selledNum =str(sort.xpath('./div[@class="info"]/p[@class="selledNum"]/text()')[0])
        dict= {'top':top,'name':text,'价格':cost,'销量':selledNum}
        products.append(dict)
    return products

def Analysis(products):
    pass
if __name__ == '__main__':
    wb=taobao_login()
    products=taobao_getdata(wb)
    print(products)
    Analysis(products)


###验证码绕不过去
#再打开一个页
# wb.get('http://www.baidu.com')
# wb.back()#回退  回到前一页
# wb.forward()# 前进  再回到baidu.com
# #定们包含 iframe的标签
# wb.get('https://www.w3school.com.cn/tiy/t.asp?f=hdom_body_classname')
# wb.switch_to.frame('iframeResult')
# script=wb.find_element_by_id('myid')
# print(script.text)


#wb.close()

