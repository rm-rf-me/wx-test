from config import TOKEN, XML_STR, ONE_INFO, MAIN_INFO, INFO
from flask import Flask, request, make_response

import hashlib
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/wx', methods=['GET', 'POST'])
def chatme():
    if request.method == 'GET':
        data = request.args
        token = TOKEN
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')  
        nonce = data.get('nonce', '')  
        echostr = data.get('echostr', '')
        s = [timestamp, nonce, token]
        s = ''.join(s).encode("utf-8")

        if hashlib.sha1(s).hexdigest() == signature:
            return make_response(echostr)

        else:
            return make_response("signature validation error")

    if request.method == 'POST':
        xml_str = request.stream.read()
        xml = ET.fromstring(xml_str)
        toUserName = xml.find('ToUserName').text
        fromUserName = xml.find('FromUserName').text
        createTime = xml.find('CreateTime').text
        msgType = xml.find('MsgType').text

        if msgType != 'text':
            reply = XML_STR % (
                fromUserName,
                toUserName,
                createTime,
                'text',
                'Unknow Format, Please check out'
            )
            return reply

        else:
            content = xml.find('Content').text
            msgId = xml.find('MsgId').text
            totOpNum = 5

            if u'游泳社' in content:
                content = '小白：游泳社yyds！'
                return XML_STR % (fromUserName, toUserName, createTime, msgType, content)
            if u'吗' in content or u'?' in content or u'？' in content:
                content = "小白：" + content.strip('吗?？')+"!"
                return XML_STR % (fromUserName, toUserName, createTime, msgType, content)

            if u'查看菜单' in content:
                content = '回复"小白+数字"查看对应信息（如"小白+1")：\n1:QQ群号\n2:游泳社春季学期活动简介\n3:教学活动简介\n4:约游活动简介\n5:深水突击活动简介\n'
                return XML_STR % (fromUserName, toUserName, createTime, msgType, content)
            
            if u'小白+' in content:
                op = int(content[-1])
                if op > 0 and op <= totOpNum:
                    # if op == 1:
                    #     content = MAIN_INFO
                    # else if op == 2:
                    #     content = ONE_INFO
                    content = INFO[op]
                else :
                    content = '请输入正确的命令，如"小白+1"'
                return XML_STR % (fromUserName, toUserName, createTime, msgType, content)

            if type(content).__name__ == "unicode":
                content = content[::-1]
                content = content.encode('UTF-8')
            elif type(content).__name__ == "str":
                print(type(content).__name__)
                content = content
                content = content[::-1]

        content = "后端小白正在开发中，目前这个程序还比较呆，它大部分情况会倒着重复你的话，偶尔可能会和你聊一会。\n或者你可以发送“查看菜单”来看看现在小白能干什么。所以有什么问题请加QQ群：983352543询问。\n\n小白："+content
        reply = XML_STR % (fromUserName, toUserName, createTime, msgType, content)
        return reply

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

        