import pytesseract
import requests as req
from PIL import Image
#未执行通过
def get_codetext1(picturepath):
    # 1、指定 tesseract.exe 文件的所在路径
    #pytesseract.pytesseract.tesseract_cmd = "D:/Programs/Python/Python37/Scripts/pytesseract.exe"
    image = Image.open(picturepath)
    text = pytesseract.image_to_string(image)
    print(text)
    return text
if __name__ == '__main__':
    get_codetext1('./testcode1.png')