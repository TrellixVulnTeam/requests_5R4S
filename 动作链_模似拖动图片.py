from selenium import  webdriver
from selenium.webdriver import ActionChains
import random

from lxml import etree
import re,time,sys
def random_int():
    return random.randint(-2,5)

if __name__ == '__main__':
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 允许开发者模式
    brow = webdriver.Chrome(executable_path='../chromedriver.exe', options=chrome_option)
    # #模拟鼠标滚动一页
    # wb.execute_script('window.scrollTo(0,document.body.scrollHeight)') #滚动一屏，加一些无相关的操作，模拟人工
    brow.execute_script('Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) ')  #将属性设置为非webdriver 方式，（淘宝针对这个有反爬机制）
    brow.get()
    #切换到iframe
    brow.switch_to.frame('')
    #实例化一个动作链
    action=ActionChains(brow)
    #找到要执行动作链的标签（可拖动对象）
    click=brow.find_element_by_css_selector('')
    #执行动作链操作
    action.click_and_hold(click)
    #开始执行动作链
    for i in range(20):
        action.move_by_offset(xoffset=random_int(),yoffset=0).perform()   #水平移动y 为0
        time.sleep(random.randint(1,5)/5)
    brow.close()

    time.sleep(3)
