from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction

import configparser

import random

import time

import requests

import urllib3

from urllib.parse import quote
app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

# mydb = mysql.connector.connect(
  # host="localhost",
  # user="root",
  # password="root",
  # database="linebot"
# )

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        image_url_1 = "https://imgur.com/Qxk3P52.jpg"
        # Phoebe 愛唱歌
        pretty_note = '♫♪♬'
        pretty_text = ''
        user_id = event.source.user_id
        textcontent =""
        
        # mycursor = mydb.cursor()
        # sql = "INSERT INTO `users`(`ID`) VALUES ("+"'"+user_id+"'"+")"
        # mycursor.execute(sql,str(user_id))
        # mydb.commit()
        
        # for i in event.message.text:
        
            # pretty_text += i
            # pretty_text += random.choice(pretty_note)
            
        moth=time.strftime("%m/%d", time.localtime())
        min=time.strftime("%H:%M",time.localtime())
        textname="徐聖凱"+moth+" "+min+"已進入實驗室"
        # myTeamsMessage = pymsteams.connectorcard("https://outlook.office.com/webhook/345a469f-3798-4fbf-a824-7cc0616d4fc9@b467d443-c70e-463e-88bd-991067d94fbb/IncomingWebhook/0949379fa9da44a48f518770cc4220b9/cfacdd03-f1f1-41b9-9acb-466e84bddabc")
        # myTeamsMessage.text(textname)
        # myTeamsMessage.send()
        
        url ="https://shopee.tw/api/v2/search_items/?keyword="+event.message.text+"&by=price&limit=50&locations=-1&newest=0&order=asc&page_type=search&rating_filter=1&version=2"
        header = {
            'if-none-match-': '55b03-634508b9798ba9f4e118b697a946c895',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
        }
        req = requests.get(url, headers = header)
        print(req.status_code)
        data = req.json()
        if data['total_count']>0:
            itemlen=3
            if data['total_count']<3:
                itemlen=data['total_count']
            for i in range(itemlen):
                itemurl=data['items'][i]['name']+"-i."+str(data['items'][i]['shopid'])+"."+str(data['items'][i]['itemid'])
                itemurl=quote(itemurl)
                itemurl="https://shopee.tw/"+itemurl
                header = {
                    'Content-Type': 'application/json',
                    'reurl-api-key': '4070ff49d794e33618563b663c974755ecd3b735939904df8a38b58d65165567c4f5d6',
                }
                obj={"url":itemurl,"utm_source":"FB_AD"}
                regg = requests.post("https://api.reurl.cc/shorten", headers = header,json=obj)
                gg = regg.json()
                print('name = {}, \nPrice = {}'.format(data['items'][i]['name'],data['items'][i]['price']/100000))
                textcontent=textcontent+str(data['items'][i]['name'])+"\n價錢:"+str(int(data['items'][i]['price']/100000))+"\n"+gg['short_url']+"\n\n"
        else:
            textcontent="你他媽別亂打"
       
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=textcontent)
        )

if __name__ == "__main__":
    app.run()