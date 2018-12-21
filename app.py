# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import random
import time
from pymongo import MongoClient

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

mongo_url = os.getenv('MONGODB_URI', None)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        text=event.message.text
        user_id = event.source.user_id
        if math_get_data(user_id) == None:
            data = dict()
            x = random.randint(1, 10)+10
            y = random.randint(1, 10)
            data['uuid'] = user_id
            data['x'] = x
            data['y'] = y
            data['Ans'] = x+y 
            data['count']=1
            data['ok_count']=0
            data['ng_count']=0
            math_insert_data(data)

        if(text=='math'):
            content = 'hi~ [%s] 你好，開始進行數學測驗\n' %(user_id)

            data = None
            try:
                data = math_get_data(user_id)
            except Exception as e:
                print('ex: ', str(e))

            # save to db
            if data:
                x = random.randint(1, 10)+10
                y = random.randint(1, 10)
                if 'x_min' in data:
                    x = random.randint(data['x_min'], data['x_max'])
                if 'y_min' in data:
                    y = random.randint(data['y_min'], data['y_max'])
                data['uuid'] = user_id
                data['x'] = x
                data['y'] = y
                data['Ans'] = x+y
                data['count']=1
                data['ok_count']=0
                data['ng_count']=0
            else:
                data = dict()
                x = random.randint(1, 10)+10
                y = random.randint(1, 10)
                data['uuid'] = user_id
                data['x'] = x
                data['y'] = y
                data['Ans'] = x+y 
                data['count']=1
                data['ok_count']=0
                data['ng_count']=0
            math_insert_data(data)
            # make line message
            content += '%s + %s = ' %(x, y)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content)
            )
        elif(text.startswith('#x')):
            content = 'hi~ [%s] 你好\n' %(user_id)
            items = text.split(',')
            x_min = int(items[1])
            x_max = int(items[2])
            # save to db
            #data = dict()
            data = None
            try:
                data = math_get_data(user_id)
            except Exception as e:
                print('ex: ', str(e))

            if data:
                data['x_min'] = x_min
                data['x_max'] = x_max
            else:
                data = dict()
                data['uuid'] = user_id
                data['count']=0
                data['ok_count']=0
                data['ng_count']=0
                data['x_min'] = x_min
                data['x_max'] = x_max
            math_insert_data(data)

            # line message
            content += "已設定x範圍為%s~%s\n" %(x_min, x_max)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content)
            )
        elif(text.startswith('#y')):
            content = 'hi~ [%s] 你好\n' %(user_id)
            items = text.split(',')
            y_min = int(items[1])
            y_max = int(items[2])
            # save to db
            data = None
            try:
                data = math_get_data(user_id)
            except Exception as e:
                print('ex: ', str(e))

            if data:
                data['y_min'] = y_min
                data['y_max'] = y_max
            else:
                data = dict()
                data['uuid'] = user_id
                data['count']=0
                data['ok_count']=0
                data['ng_count']=0
                data['y_min'] = y_min
                data['y_max'] = y_max
            math_insert_data(data)

            # line message
            content += "已設定y範圍為%s~%s\n" %(y_min, y_max)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content)
            )
        elif(text=='test'):
            content = 'hi~ '#+'['+userId+'], '
            content += 'id(%s) = %s\n' %(type(event.source.user_id), event.source.user_id)
            content += text +'\n'
            x = random.randint(1, 10)
            y = random.randint(1, 10)
            content += '%s + %s = ' %(x, y)
            content += '\n' + str(body)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content)
            )
        else:
            data = None
            try:
                data = math_get_data(user_id)
            except Exception as e:
                print('ex: ', str(e))

            # data != None, deal it
            # data['count']>0表示已有出過題了，正在作達中
            if data and data['count']>0:
                if(text.isdigit()):
                    content = ''
                    if(data['Ans'] == int(text) ):
                        data['ok_count'] += 1
                        content += 'OK\n'
                    else:
                        data['ng_count'] += 1
                        content += '正確答案是：%s\n' %(data['x']+data['y'])
                    if(data['count']<5):
                        content += "==== 下一題 ====\n"
                        x = random.randint(1, 10)+10
                        y = random.randint(1, 10)
                        if 'x_min' in data:
                            x = random.randint(data['x_min'], data['x_max'])
                        if 'y_min' in data:
                            y = random.randint(data['y_min'], data['y_max'])

                        content += '%s + %s = ' %(x, y)
                        # save to db
                        data['x'] = x
                        data['y'] = y
                        data['Ans'] = x+y
                        data['count']+=1
                        math_insert_data(data)
                    else:
                        content += "==== 測驗結束 ====\n"
                        content += '答對 %s 題\n' %(data['ok_count'])
                        content += '答錯 %s 題\n' %(data['ng_count'])
                        # remove 'uuid' data
                        #math_remove_data(data['uuid'])
                        # reset count
                        data['count'] = 0
                        math_insert_data(data)

                        # 煙火圖 'https://i.imgur.com/mqa7jIQ.jpg'
                        url = 'https://i.imgur.com/mqa7jIQ.jpg'
                        image_message = ImageSendMessage(
                            original_content_url=url,
                            preview_image_url=url
                        )

                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=content)
                    )

            else:
                content = '請送出 math 指令，開始測驗'
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=content)
                )


    return 'OK'


def math_insert_data(my_data):
    client = MongoClient(mongo_url)
    db = client[mongo_url.split('/')[-1]]
    # history data
    uuid = my_data['uuid']#'malo.home1'
    my_coll = db[uuid] #get collection
    my_coll.remove( {'uuid':my_data['uuid']} ) # remove all items (documents)
    res = my_coll.insert(my_data)

def math_get_data(uuid):
    data = None
    try:
        client = MongoClient(mongo_url)
        db = client[mongo_url.split('/')[-1]]
        my_coll = db[uuid] #get collection
        res = my_coll.find() #全抓
        data = list(res)[0]
        data.pop('_id')
        print('data: ', data)
    except Exception as e:
        return None
    return data

def math_remove_data(uuid):
    client = MongoClient(mongo_url)
    db = client[mongo_url.split('/')[-1]]
    # history data
    my_coll = db[uuid] #get collection
    my_coll.remove( {'uuid':uuid} ) # remove all items (documents)


@app.route("/", methods=['GET'])
def basic_url():
    return 'OK'


if __name__ == "__main__":
    app.run()
