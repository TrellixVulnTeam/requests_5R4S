from aip import AipOcr
'''pip3 install baidu-aip'''

""" 你的 APPID AK SK """
APP_ID = '23581870'
API_KEY = 'kRamexd4gjzUkZjmbF6ZeBkQ'
SECRET_KEY = 'biwIv4HLUvmceOBAzCv75kFMulYn7szx'

def get_codetext1(filePath):
    image =  open(filePath, 'rb').read()
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    #client.basicGeneral(image); #普通识别
    """ 调用通用文字识别（高精度版） """  #个人已购买1年
    text=client.basicAccurate(image)['words_result'][0]['words'];

    print('识别结果：',text)
    return text
if __name__ == '__main__':
    text=get_codetext1('./testcode1.png')

"""使用说明地址：http://ai.baidu.com/ai-doc/OCR/7kibizyfm
     带参数调用通用文字识别, 图片参数为本地图片 
    client.basicGeneral(image, options)
url = "https//www.x.com/sample.jpg" 
调用通用文字识别, 图片参数为远程url图片 
    client.basicGeneralUrl(url);
带参数调用通用文字识别, 图片参数为远程url图片 
client.basicGeneralUrl(url, options)"""
""" 调用身份证识别 
client.idcard(image, idCardSide);"""

""" 调用银行卡识别 
client.bankcard(image);"""

""" 调用驾驶证识别 
client.drivingLicense(image);"""

""" 调用行驶证识别 
client.vehicleLicense(image);"""


""" 调用车牌识别
client.licensePlate(image); """

""" 调用营业执照识别
client.businessLicense(image); """

""" 调用通用票据识别
client.receipt(image); """

""" 调用表格文字识别同步接口 
client.form(image);"""

""" 调用表格文字识别 
client.tableRecognitionAsync(image);"""

""" 试卷分析与识别 调用文档版面分析与识别, 入参为图片
    client.docAnalysis(image);"""

""" 调用仪器仪表盘读数识别, 入参为图片
    client.meter(image);"""

""" 调用网络图片文字识别（含位置版）, 入参为图片
    client.webimageLoc(image);"""
