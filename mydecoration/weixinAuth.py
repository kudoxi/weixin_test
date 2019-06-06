from django.http import HttpResponseRedirect,HttpResponse,HttpResponseRedirect
from weixin_test.settings import *
from urllib import parse,request
import json
import os,sys,io
'''
微信鉴权
'''
def weixin_auth(func):
    def wrapper(req,*args,**kwargs):
        userid = req.session.get('userid')
        if not userid:

            redirect_url = 'http://127.0.0.1:8080'+req.get_full_path()
            url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri={}&response_type=code&scope=snsapi_base&state=123#wechat_redirect'\
                .format(APPID,redirect_url)
            print(url)
            #return HttpResponseRedirect(url);
            #urlResp = request.urlopen(url)
            #urlResp_text = urlResp.read().decode('gbk')
            #print('urlResp_text:',urlResp_text)
            #urlResp = json.loads(urlResp_text)


        return  func(req,*args, **kwargs)
    return wrapper


