from django.shortcuts import render
from django.http import request,HttpResponse
from utils.WeixinAuth import Weixin
from mydecoration.weixinAuth import *
from weixin_test.settings import *
import logging
import hashlib



#https://blog.csdn.net/u013538542/article/details/86983806
# Create your views here.
@weixin_auth
def index(req):
    wx = Weixin()
    access_token = wx.get_access_token(req)
    print('access_token',access_token)
    return HttpResponse(8888)
    #return HttpResponse('access_token:{}'.format(access_token))

#回复微信应答
def answer(req):
    logging.info("--------req:"+req.get)
    signature = req.get("signature")
    timestamp = req.get("timestamp")
    nonce = req.get("nonce")
    echostr = req.get("echostr")
    token = TOKEN
    words = [token,timestamp,nonce]
    words.sort()
    logging.info("--------words:"+words)
    sha1 = hashlib.sha1()
    map(sha1.update, words)
    hashcode = sha1.hexdigest()
    print("handle/GET func: hashcode, signature: ", hashcode, signature)
    if hashcode == signature:
        return echostr
    else:
        return ""




def access_token(req):
    logger = logging.getLogger('django')
    logger.info('-------------------------test')
    return HttpResponse(2222)

