from selenium import webdriver
import requests,json
from time import sleep
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import cv2
import numpy as np
from io import BytesIO
import time, requests

chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 允许开发者模式
brow = webdriver.Chrome(executable_path='../chromedriver.exe', options=chrome_option)
brow.execute_script('Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) ') #将WEBDRIVER 属性置为false

configfile='D:/logininfo.json'
#读取json格式的配置文件

def file2dict(configfile):
    jsoncontent=[]
    with open(configfile, encoding="utf-8") as f:
        jsoncontent=json.load(f)
        #if jsoncontent.startswith(u'\ufeff'):
        #     jsoncontent = jsoncontent.encode('utf8')[3:].decode('utf8')
        return jsoncontent

def saveimg(brow):
    # 找到验证码两张图片（要拖动的与原背景图）并保存
    target = brow.find_element_by_id('slideBlock')
    template = brow.find_element_by_id('slideBg')
    target_link = target.get_attribute('src')
    template_link = str(template.get_attribute('src')).split('**')[0]
    print(template_link)
    target_img = Image.open(BytesIO(requests.get(target_link).content))
    template_img = Image.open(BytesIO(requests.get(template_link).content))
    target_img.save('target.png')
    template_img.save('template.png')
    local_img = Image.open('target.png')
    size_loc = local_img.size
    #brow.zoom = 320 / int(size_loc[0])
    brow.zoom = 280
def logininqqzone():
    url='https://i.qq.com/'
    brow.get(url)
    brow.switch_to.frame('login_frame')
    brow.find_element_by_id('switcher_plogin').click() #找到账户密码登录 ，并点击
    logininfo=file2dict(configfile)
    username=logininfo['qquser']
    password=logininfo['qqpassword']
    sleep(1)
    brow.find_element_by_id('u').send_keys(username) #找到用户名输入框并输入用户名
    sleep(1)
    brow.find_element_by_id('p').send_keys(password) #找到密码输入框并输入密码
    sleep(1)
    brow.find_element_by_id('login_button').click() #找到登录按钮，点击
    sleep(1)
    brow.execute_script(
        'Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) ')  # 将WEBDRIVER 属性置为false
    #brow.switch_to.parent_frame()
    loginiframe=brow.find_element_by_tag_name('iframe')
    brow.switch_to.frame(loginiframe)
    #brow.switch_to.frame('tcaptcha_iframe')
    #找到验证码两张图片（要拖动的与原背景图）并保存
    saveimg(brow)

def get_tracks( distance):
    print(distance)
    distance += 20
    v = 0
    t = 0.2
    forward_tracks = []
    current = 0
    mid = distance * 3 / 5  #减速阀值
    while current < distance:
        if current < mid:
            a = 2  #加速度为+2
        else:
            a = -3  #加速度-3
        s  = v * t + 0.5 * a * (t ** 2)
        v = v + a * t
        current += s
        forward_tracks.append(round(s))

    back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
    return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}

def match(target, template):
    img_rgb = cv2.imread(target)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template, 0)
    run = 1
    w, h = template.shape[::-1]
    print(w, h)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    run = 1

    # 使用二分法查找阈值的精确值
    L = 0
    R = 1
    while run < 15:
        run += 1
        threshold = (R + L) / 2
        print(threshold)
        if threshold < 0:
            print('Error')
            return None
        loc = np.where(res >= threshold)
        print(len(loc[1]))
        if len(loc[1]) > 1:
            L += (R - L) / 2
        elif len(loc[1]) == 1:
            print('目标区域起点x坐标为：%d' % loc[1][0])
            break
        elif len(loc[1]) < 1:
            R -= (R - L) / 2
    return loc[1][0]

def crack_slider(brow):
    slider = brow.find_element_by_id('slideBlock')
    ActionChains(brow).click_and_hold(slider).perform()

    for track in tracks['forward_tracks']:
        ActionChains(brow).move_by_offset(xoffset=track, yoffset=0).perform()

    time.sleep(0.3)
    for back_tracks in tracks['back_tracks']:
        ActionChains(brow).move_by_offset(xoffset=back_tracks, yoffset=0).perform()

    ActionChains(brow).move_by_offset(xoffset=-4, yoffset=0).perform()
    ActionChains(brow).move_by_offset(xoffset=4, yoffset=0).perform()
    time.sleep(3)
    ActionChains(brow).release().perform()

        #识别验证码
class CrackSlider():
    """
    通过浏览器截图，识别验证码中缺口位置，获取需要滑动距离，并模仿人类行为破解滑动验证码
    """
    def __init__(self,url,brow):
        self.url = url
        self.driver = brow
        self.driver.execute_script('Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) ') #将WEBDRIVER 属性置为false
        self.wait = WebDriverWait(self.driver, 20)
        self.zoom = 1

    def open(self):
        self.driver.get(self.url)
        #self.driver.switch_to.frame('switcher_plogin')
        self.driver.switch_to.frame(1)
    def get_pic(self):
        time.sleep(2)
        self.driver.switch_to.frame('login_frame')
        self.driver.switch_to.frame('tcaptcha_iframe')
        target = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tc-jpp-img unselectable')))
        template = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tc-bg-img unselectable')))
        target_link = target.get_attribute('src')
        template_link = template.get_attribute('src')
        target_img = Image.open(BytesIO(requests.get(target_link).content))
        template_img = Image.open(BytesIO(requests.get(template_link).content))
        target_img.save('target.jpg')
        template_img.save('template.png')
        local_img = Image.open('target.jpg')
        size_loc = local_img.size
        self.zoom = 320 / int(size_loc[0])

    def get_tracks(self, distance):
        print(distance)
        distance += 20
        v = 0
        t = 0.2
        forward_tracks = []
        current = 0
        mid = distance * 3 / 5  #减速阀值
        while current < distance:
            if current < mid:
                a = 2  #加速度为+2
            else:
                a = -3  #加速度-3
            s  = v * t + 0.5 * a * (t ** 2)
            v = v + a * t
            current += s
            forward_tracks.append(round(s))

        back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
        return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}

    def match(self, target, template):
        img_rgb = cv2.imread(target)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template, 0)
        run = 1
        w, h = template.shape[::-1]
        print(w, h)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        run = 1

        # 使用二分法查找阈值的精确值
        L = 0
        R = 1
        while run < 20:
            run += 1
            threshold = (R + L) / 2
            print(threshold)
            if threshold < 0:
                print('Error')
                return None
            loc = np.where(res >= threshold)
            print(len(loc[1]))
            if len(loc[1]) > 1:
                L += (R - L) / 2
            elif len(loc[1]) == 1:
                print('目标区域起点x坐标为：%d' % loc[1][0])
                break
            elif len(loc[1]) < 1:
                R -= (R - L) / 2
        return loc[1][0]

    def crack_slider(self):
        slider = brow.find_element_by_id('slideBlock')
        ActionChains(self.driver).click_and_hold(slider).perform()

        for track in tracks['forward_tracks']:
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()

        time.sleep(0.5)
        for back_tracks in tracks['back_tracks']:
            ActionChains(self.driver).move_by_offset(xoffset=back_tracks, yoffset=0).perform()

        ActionChains(self.driver).move_by_offset(xoffset=-4, yoffset=0).perform()
        ActionChains(self.driver).move_by_offset(xoffset=4, yoffset=0).perform()
        time.sleep(0.5)

        ActionChains(self.driver).release().perform()

        #识别验证码


if __name__ == '__main__':

    logininqqzone()  #打开登录页输入用户信息，并找到验证码图片保存
    target = 'target.png'  # 保存后的图
    template = 'template.png'
    distance = match(target, template)
    tracks = get_tracks((distance) * brow.zoom)  # 对位移的缩放计算
    tracks = get_tracks((distance) )  # 对位移的缩放计算
    crack_slider(brow)


    #brow.close()