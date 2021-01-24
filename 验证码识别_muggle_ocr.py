'''只能识别简单的文字，不支持滑动与计算'''
import time
#from tensorflow.python._pywrap_tensorflow_internal import *
'''麻瓜库安装  
step 1 pip3 install tensorflow==2.0 # 要指定版本，最新版本不兼容
step2: pip3 install muggle_ocr  
有400MB左右
可以识别非常简单的
'''
import  muggle_ocr    #使用麻瓜库

"""
使用预置模型，预置模型包含了[ModelType.OCR, ModelType.Captcha] 两种
其中 ModelType.OCR 用于识别普通印刷文本, ModelType.Captcha 用于识别4-6位简单英数验证码

"""
def get_textcode1(picturepath):
    # 打开印刷文本图片
    with open(picturepath, "rb") as f:
        ocr_bytes = f.read()
    # 2. 初始化；model_type 可选: [ModelType.OCR, ModelType.Captcha]
    sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.OCR)
    # ModelType.Captcha 可识别光学印刷文本

    text = sdk.predict(image_bytes=ocr_bytes)
    print(text)
    return text

def get_textcode2(picturepath):
    # 打开验证码图片
    with open(picturepath, "rb") as f:
        captcha_bytes = f.read()
    # ModelType.Captcha 可识别4-6位验证码
    sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

    text = sdk.predict(image_bytes=captcha_bytes)
    print(text)
    return text
"""
使用自定义模型
支持基于 https://github.com/kerlomz/captcha_trainer 框架训练的模型
训练完成后，进入导出编译模型的[out]路径下, 把[graph]路径下的pb模型和[model]下的yaml配置文件放到同一路径下。
将 conf_path 参数指定为 yaml配置文件 的绝对或项目相对路径即可，其他步骤一致，如下示例：
"""
def get_textcode3(picturepath):
    with open(picturepath, "rb") as f:
        b = f.read()
    sdk = muggle_ocr.SDK(conf_path="./ocr.yaml")
    text = sdk.predict(image_bytes=b)
    return text
if __name__ == '__main__':
    get_textcode2('testcode1.png')