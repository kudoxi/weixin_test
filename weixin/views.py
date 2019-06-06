from django.shortcuts import render
from django.http import request,HttpResponse
from utils.WeixinAuth import Weixin
from mydecoration.weixinAuth import *
import logging
# Create your views here.
'''
@weixin_auth
def index(req):
    wx = Weixin()
    access_token = wx.get_access_token(req)
    print('access_token',access_token)
    return HttpResponse(8888)
    #return HttpResponse('access_token:{}'.format(access_token))
'''

def access_token(req):
    logger = logging.getLogger('django')
    logger.info('-------------------------test')
    return HttpResponse(2222)
