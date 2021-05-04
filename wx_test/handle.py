import hashlib
import reply
import receive
import web
import time
class Handle(object):
    def POST(self):
        try:
            webData = web.data()
            print ("Handle Post webdata is ", webData)
            #后台打日志
            recMsg = receive.parse_xml(webData)
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                textt = recMsg.Content
                print ("text:", textt)
                with open ("tmp.txt", "a+") as f:
                    f.writelines ("to: "+str(fromUser)+" from: "+str(toUser)+" time: "+time.asctime( time.localtime(time.time()) )+" text: "+str(textt)+'\n') 
                f.close()
                content = "程序猿正在狂修后端代码，获取推送请见推送历史，咨询请加QQ群：983352543"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                content = "憋发了这个辣鸡后端现在只能收文本消息。。。"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
        except Exception as Argment:
            return Argment
