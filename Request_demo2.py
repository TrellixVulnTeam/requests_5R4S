import requests
import re



def get_result(key):
    pass

#get 请求，带UserAgent
if __name__ == '__main__':
    url="https://fanyi.sogou.com/?transfrom=auto&transto=zh-CHS&model=general&"
    headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Mobile Safari/537.36'}
    keyworld=input("请输入要查询的关键字：")
    para={
        'keyword':keyworld
    }

    response=requests.get(url=url,params=para,headers=headers)
    print(response.url)
    page_text=response.text
    print(page_text)
    rex=r"'word-class\'>v\.<\/span>\ (.+?)"
    text=re.findall(rex,page_text)
    print(text)
    with open("sogou_reuqest"+keyworld+".html",'w',encoding='UTF-8') as fw:
        fw.write(keyworld+":"+str(text))
