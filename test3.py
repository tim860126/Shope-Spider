import requests
import pandas as pd
import zhconv

url ="https://shopee.tw/api/v2/search_items/?keyword=太鼓&by=price&limit=50&locations=-1&newest=0&order=asc&page_type=search&rating_filter=1&version=2"
header = {
    'if-none-match-': '55b03-634508b9798ba9f4e118b697a946c895',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
}
req = requests.get(url, headers = header)
print(req.status_code)
data = req.json()
df = pd.DataFrame()
for page in range(data['total_count']//50+1):
    url1 ="https://shopee.tw/api/v2/search_items/?keyword=太鼓&by=price&limit=50&locations=-1&newest="
    urlpage=page*50
    url2="&order=asc&page_type=search&rating_filter=1&version=2"
    url=url1+str(urlpage)+url2
    req = requests.get(url, headers = header) 
    data = req.json()
    for i in range(len(data['items'])):
        itemurl="https://shopee.tw/"+data['items'][i]['name']+"-i."+str(data['items'][i]['shopid'])+"."+str(data['items'][i]['itemid'])
        ps=pd.DataFrame([{'Name':data['items'][i]['name'],'Price':data['items'][i]['price']/100000,'url':itemurl}],columns=['Name','Price','url'])
        df = df.append(ps,ignore_index=True)
        print('name = {}, \nPrice = {}'.format(data['items'][i]['name'],data['items'][i]['price']/100000))
df.to_excel('index2.xlsx',index = False)

frame=df.sort_values('Price',ascending=True).index


