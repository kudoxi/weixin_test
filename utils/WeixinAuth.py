from urllib import parse,request
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import json
from time import time,gmtime
from datetime import datetime
import requests
from weixin_test.settings import *

class Weixin:
    def __init__(self):
        self.logger = logging.getLogger('django')

    '''
        网页授权 access_token 信息
        返回：{'access_token': 'xxxxx', 'refresh_token': 'xxxxxxxxxx', 'scope': 'snsapi_userinfo', 'expires_in': 7200, 'openid': 'oe1Rp6Pv6_Dp2baNz7sCTTOo5mxk'}
    '''
    def get_access_token_info(self,req,code):
        logger = self.logger
        curl = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code' \
            .format(APPID, APPSECRET, code)
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
        req.session['openid'] = openid
        return urlResp

    '''
        根据 refresh_token 获取 网页授权 access_token
    '''
    def get_access_token_by_refresh(self,req):
        logger = self.logger
        expires_in = req.session.get('access_token_expires_in','')
        access_token = req.session.get('access_token','')
        refresh_token_expires_in = req.session.get('refresh_token_expires_in','')
        refresh_token = req.session.get('refresh_token','')
        now = time()

        if not access_token or (now < refresh_token_expires_in):
            #refresh_token 过期，需要重新鉴权
            code= req.session.get("code")
            tokenResp = self.get_access_token_info(req,code)
            access_token = tokenResp['access_token']
        else:
            if now < expires_in:
                #如果只是 access_token 过期
                url = "https://api.weixin.qq.com/sns/oauth2/refresh_token?appid={}&grant_type=refresh_token&refresh_token={}"\
                    .format(APPID,refresh_token)
                res = requests.get(url)
                res2 = res.text
                tokenResp = json.loads(res2)
                logger.info("--------------get tokenResp:")
                logger.info(tokenResp)
                access_token = tokenResp['access_token']
                openid = tokenResp['openid']
                req.session['access_token'] = access_token
                req.session['openid'] = openid
        return access_token


    '''
        获取用户信息 userinfo
        返回：{'sex': 2, 'city': '', 'nickname': 'xxxxx', 'openid': 'oe1Rp6Pv6_Dp2baNz7sCTTOo5mxk', 'province': 'xxx', 'privilege': [], 'language': 'zh_CN', 'headimgurl': 'http://thirdwx.qlogo.cn/mmopen/vi_32/xxxx', 'country': 'xxxx'}
    '''
    def get_userinfo(self,req,access_token,openid):
        logger = self.logger
        # 获取用户信息
        userinfo_url = 'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}&lang=zh_CN' \
            .format(access_token, openid)
        userres = requests.get(userinfo_url)
        userres2 = userres.text
        userResp = json.loads(userres2)
        logger.info("--------------get userResp:")
        logger.info(userResp)
        return userResp