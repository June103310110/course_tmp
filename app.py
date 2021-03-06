from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('n/LnYr4PB08RFunptSQU1CiTD98N4gaJQ4AmixCeQJKLmYJuUq56DGoMFQHsghmFcCgV2caiE/B4NeUQVGCyKOXFQ4DJTm0w5CoXQlBVyyht7ZL+EIiNkMUBi3xHgLCUqwB87jBAbXtV90GpBGGt1QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('97e16b060f49eee4a9d016cee1478a81')

# 推給你自己 
line_bot_api.push_message('Uf7ed79507d4604d7ad583f14863e2595', TextSendMessage(text='(後臺訊息)啟動豆芽探索共學ECHO機器人!'))

# 推給某個User
# line_bot_api.push_message('UserID', TextSendMessage(text='(後臺訊息)啟動豆芽探索共學ECHO機器人!'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
      # get user id when reply
    user_id = event.source.user_id
    print("user_id =", user_id)
    
    reply_msg = event.message.text+'\nyour User ID is '+user_id+\
                    ' \n輸入「你好」會啟動reply_message回復「不錯喔」'
    
    if event.message.text=='你好':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='不錯喔'))
    
    image_url = 'https://i.imgur.com/d3vfgZP.png'
    try:
        line_bot_api.push_message(user_id, ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
    except LineBotApiError as e:
        # error handle
        raise e
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
© 2021 GitHub, Inc.
