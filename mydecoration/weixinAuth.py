from django.http import HttpResponseRedirect,HttpResponse,HttpResponseRedirect
from weixin_test.settings import *
from urllib import parse,request
import json
import os,sys,io
import requests
import logging
from time import time
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
            code = req.GET.get("code",'')
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
                logger.info("--------------get urlResp:")
                logger.info(urlResp)
                refresh_token = urlResp['refresh_token']
                access_token = urlResp['access_token']
                expires_in = urlResp['expires_in']
                openid = urlResp['openid']
                now = time()
                expires_in = now + expires_in
                refresh_token_expires_in = now + 60 * 60 * 24 * 30
                req.session['access_token_expires_in'] = expires_in
                req.session['access_token'] = access_token
                req.session['refresh_token_expires_in'] = refresh_token_expires_in
                req.session['refresh_token'] = refresh_token
                #获取用户信息
                userinfo_url = 'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}&lang=zh_CN'\
                    .format(access_token,openid)
                userres = requests.get(userinfo_url)
                userres2 = userres.text
                userResp = json.loads(userres2)
                logger.info("--------------get userResp:")
                logger.info(userResp)
        else:
            pass
            # #超过刷新时间就要重新请求
            # if now < refresh_token_expires_in:
            #     pass
            # else:
            #     #短暂超时，用refresh_token获取新access_token
            #     if now < expires_in:
            #         pass



        return  func(req,*args, **kwargs)
    return wrapper


