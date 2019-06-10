from django.http import HttpResponseRedirect,HttpResponse,HttpResponseRedirect
from weixin_test.settings import *
from urllib import parse,request
import json
import os,sys,io
import requests
import logging
'''
微信鉴权
'''
def weixin_auth(func):
    def wrapper(req,*args,**kwargs):
        userid = req.session.get('userid')
        if not userid:
            logger = logging.getLogger('django')
            redirect_url = ROOT_URL+"/weixin_test"+req.get_full_path()
            redirect_uri = 'https://xscenic.qiweiwangguo.com/cas_api/v1/wechat/auth'
            url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri={}&response_type=code&scope={}&state=123#wechat_redirect'\
                .format(APPID,redirect_url,SCOPE)
            logger.info('-------------------------url:'+url)
            code = req.GET.get("code")
            if not code:
                return HttpResponseRedirect(url)
            else:
                logger.info("---------------get code:"+code)
                # 3.通过code换取网页授权access_token
                curl = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'\
                    .format(APPID,APPSECRET,code)
                res = requests.get(curl)
                res2 = res.text
                urlResp = json.loads(res2)
                logger.info("--------------get urlResp:"+urlResp)
            #urlResp = request.urlopen(url)
            #urlResp_text = urlResp.read().decode('gbk')
            #print('urlResp_text:',urlResp_text)
            #urlResp = json.loads(urlResp_text)


        return  func(req,*args, **kwargs)
    return wrapper


