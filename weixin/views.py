from django.shortcuts import render
from django.http import request,HttpResponse
from utils.WeixinAuth import Weixin
from mydecoration.weixinAuth import *
import logging

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
    signature = req.get("signature")
    timestamp = req.get("timestamp")


def access_token(req):
    logger = logging.getLogger('django')
    logger.info('-------------------------test')
    return HttpResponse(2222)
