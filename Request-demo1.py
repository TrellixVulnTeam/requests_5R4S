import requests
if __name__ == '__main__':
    url="https://www.sogou.com/"
    response=requests.get(url=url)
    responsetext=response.text
    print(responsetext)
    with open('sogou.html','w',encoding='utf-8') as fw:
        fw.write(responsetext)

