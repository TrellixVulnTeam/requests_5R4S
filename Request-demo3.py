import requests
#单个单词发post 请求
def translatekeyworld(url,data,headers,keyword):

    response = requests.post(url=posturl, data=data, headers=headers).json()
    data1 = response['data']
    # print(data1)
    str = ['']
    filename = 'Translate.html'
    for i in data1:
        # print(i['v'])
        str.append(i['v'])
    print(str)
    with open(filename, 'a', encoding='utf-8') as fw:
        fw.write(keyword + ' translate to: ' + ','.join(str) + '\n')
#翻译句子
def translatesentence(url,data,headers,keyword):

    response = requests.post(url=posturl, data=data, headers=headers).json()
    #print(url)
    print(response)

    # print(data1)
    str = ['']
    filename = 'Translate.html'
    with open(filename, 'a', encoding='utf-8') as fw:
        fw.write(keyword + ' translate to: ' + ','.join(str) + '\n')

if __name__ == '__main__':

    posturl='https://fanyi.baidu.com/sug'
    headers={
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Mobile Safari/537.36'}
    print("输入单词翻译，输入 exit则退出")
    while True:
        keyword=input("please input keyword to translate:")
        str=keyword.split(' ')
        if len(str)<2:    #如果输入是单个单词则发post 请求
            data = {'kw': keyword}
            translatekeyworld(posturl, data, headers, keyword)
        elif keyword.isalnum():
            translatekeyworld(posturl, data, headers, keyword)
        else: #如果发送的是一个句子则
            url='https://fanyi.baidu.com/transapi?from=en&to=zh'
            data={'from': 'en','to': 'zh','query':keyword}
            translatesentence(url, data, headers, keyword.encode('utf-8'))