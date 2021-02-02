from selenium import webdriver
from aip import AipOcr #百度验证码识别  弱鸡
import pytesseract
from PIL import Image,ImageEnhance,ImageFilter
import time,requests
import cv2
import numpy as np
from matplotlib import pyplot as plt
####无界面模式
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
########
chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 允许开发者模式
brow = webdriver.Chrome(executable_path='../chromedriver.exe', options=chrome_option,chrome_options=chrome_options)
brow.execute_script('Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) ') #将WEBDRIVER 属性置为false

APP_ID = '23581870'
API_KEY = 'kRamexd4gjzUkZjmbF6ZeBkQ'
SECRET_KEY = 'biwIv4HLUvmceOBAzCv75kFMulYn7szx'

picturepath='./testcode3.jpg'
#去掉杂色
def delcoo(picturepath):
    img_name = picturepath
    # 去除干扰线
    im = Image.open(img_name)
    # 图像二值化
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')
    data = im.getdata()
    w, h = im.size
    # im.show()
    black_point = 0
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            mid_pixel = data[w * y + x]  # 中央像素点像素值
            if mid_pixel == 0:  # 找出上下左右四个方向像素点像素值
                top_pixel = data[w * (y - 1) + x]
                left_pixel = data[w * y + (x - 1)]
                down_pixel = data[w * (y + 1) + x]
                right_pixel = data[w * y + (x + 1)]

                # 判断上下左右的黑色像素点总个数
                if top_pixel == 0:
                    black_point += 1
                if left_pixel == 0:
                    black_point += 1
                if down_pixel == 0:
                    black_point += 1
                if right_pixel == 0:
                    black_point += 1
                if black_point >= 3:
                    im.putpixel((x, y), 0)
                # print black_point
                black_point = 0
    im.save(picturepath)

def get_codetext2(picturepath):
    # 1、指定 tesseract.exe 文件的所在路径
    #pytesseract.pytesseract.tesseract_cmd = "D:/Programs/Python/Python37/Scripts/pytesseract.exe"
    image = Image.open(picturepath)
    text = pytesseract.image_to_string(image=image)
    print(text)
    return text
#二值化
def erzihua(filePath):
    image = Image.open(filePath)
    image = image.convert('L')
    threshola = 127
    table = []
    for i in range(256):
        if i < threshola:
            table.append(0)
        else:
            table.append(1)

    image = image.point(table, '1')
    image.save(filePath)

def get_codetext1(filePath):
    image = Image.open(filePath)
    #二值化
    erzihua(filePath)
    #去掉杂色
    delcoo(picturepath)
    #image.show()

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    #client.basicGeneral(image); #普通识别
    """ 调用通用文字识别（高精度版） """  #个人已购买1年
    text=''
    try:
        text1=client.basicAccurate(image);
        print(text1)
        text=text1['words_result'][0]['words']
    except BaseException as BE:
        print(BE)
    print('识别结果：',text)
    return text

def testlogin():
    brow.get('http://www.gdchgs.com/admin/login.php')
    imgurl=brow.find_element_by_tag_name('img').get_property('src')[::]
    print(imgurl)
    saveimg=requests.get(imgurl)
    with open('./testcode3.jpg','wb') as fw:
        fw.write(saveimg.content)
    fw.close()
    testcode = get_codetext1('./testcode3.jpg')
    print(testcode)
    brow.find_element_by_name('name').send_keys('admin')
    brow.find_element_by_name('psw').send_keys('password')
    brow.find_element_by_name("text_check").send_keys(testcode)
    time.sleep(2)
    brow.find_element_by_name('Submit').click()
    time.sleep(3)
    brow.close()


if __name__ == '__main__':
    testlogin()


