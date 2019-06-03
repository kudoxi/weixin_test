from urllib import parse,request
import json
from time import time,gmtime
from datetime import datetime

class Weixin:
    def __init__(self):
        self.__accessToken = ""
        self.appId = 'wx53304857b300c82a'#'wx57f030313a9ad6c0'
        self.appSecret = '7202904ac5bad3e0fe597b5b3c309733'#'690befa4723fa2389190c0db980fbb3f'

    def __real_get_access_token(self, req):
        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
                   % (self.appId, self.appSecret))
        urlResp = request.urlopen(postUrl)
        urlResp_text = urlResp.read().decode('utf-8')
        urlResp = json.loads(urlResp_text)
        self.__accessToken = urlResp['access_token']
        self.__leftTime = urlResp['expires_in']

        req.session['access_token'] = self.__accessToken

    def get_access_token(self, req):

        token = req.session.get('access_token')
        if not token:
            self.__real_get_access_token(req)

        return self.__accessToken