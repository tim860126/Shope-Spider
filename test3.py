import requests
import pandas as pd
import zhconv

url ="https://shopee.tw/api/v2/search_items/?brandids=5005&by=sales&fe_categoryids=2185&limit=50&locations=-1&newest=0&order=desc&page_type=search&rating_filter=1&version=2"
header = {
    'if-none-match-': '55b03-634508b9798ba9f4e118b697a946c895',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
}
req = requests.get(url, headers = header)
print(req.status_code)
data = req.json()
df = pd.DataFrame()
for page in range(data['total_count']//50+1):
    url1 ="https://shopee.tw/api/v2/search_items/?brandids=5005&by=sales&fe_categoryids=2185&limit=50&locations=-1&newest="
    urlpage=page*50
    url2="&order=desc&page_type=search&rating_filter=1&version=2"
    url=url1+str(urlpage)+url2
    req = requests.get(url, headers = header) 
    data = req.json()
    for i in range(len(data['items'])):
        ps=pd.DataFrame([{'Name':zhconv.convert(data['items'][i]['name'],'zh-cn'),'Price':data['items'][i]['price']/100000}],columns=['Name','Price'])
        df = df.append(ps,ignore_index=True)
        print('name = {}, \nPrice = {}'.format(zhconv.convert(data['items'][i]['name'],'zh-cn'), data['items'][i]['price']))
df.to_excel('index2.xlsx',index = False)

print(zhconv.convert("緊張",'zh-cn'))