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
        return urlResp

    '''
        根据refresh_token 获取 网页授权 access_token
    '''
    def get_access_token_by_refresh(self,req):
        pass
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