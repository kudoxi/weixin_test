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
    logger = logging.getLogger('django')
    logger.info("-------req GET")
    logger.info(req.GET)
    signature = req.GET.get("signature",'')
    timestamp = req.GET.get("timestamp",'')
    nonce = req.GET.get("nonce",'')
    echostr = req.GET.get("echostr",'')
    logger.info("-------TOKEN:"+TOKEN)
    token = TOKEN
    words = [token,timestamp,nonce]
    words.sort()
    logger.info(words)
    sha1 = hashlib.sha1()
    sha1.update(words[0].encode("utf-8"))
    sha1.update(words[1].encode("utf-8"))
    sha1.update(words[2].encode("utf-8"))
    hashcode = sha1.hexdigest()
    logger.info("-------hashcode:"+hashcode)
    print("handle/GET func: hashcode, signature: ", hashcode, signature)
    if hashcode == signature:
        return HttpResponse(echostr)
    else:
        return HttpResponse("")


'''
    获取 code
'''
def code(req):
    logger = logging.getLogger('django')
    wx = Weixin()
    redirect_url = ROOT_URL + "/weixin_test" + req.get_full_path()
    url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri={}&response_type=code&scope={}&state=123#wechat_redirect' \
        .format(APPID, redirect_url, SCOPE)
    logger.info('-------------------------url:' + url)
    code = req.GET.get("code", '')
    if not code:
        return HttpResponseRedirect(url)
    else:
        logger.info('-------------------------code:')
        logger.info(code)
        params = {
            "meta": {
                "code": 200,
                "message": "OK"
            },
            "data": {
                "code": code,
            }
        }
    return HttpResponse(json.dumps(params), content_type='application/json')


def access_token(req):
    logger = logging.getLogger('django')
    code = req.GET.get('code','')
    if not code:
        params = {
            "meta": {
                "code": 400,
                "message": "no code"
            }
        }
        return HttpResponse(json.dumps(params), content_type='application/json')
    wx = Weixin()
    urlResp = wx.get_access_token_info(req,code)
    logger.info("--------------get urlResp:")
    logger.info(urlResp)
    params = urlResp
    return HttpResponse(json.dumps(params), content_type='application/json')


def userinfo(req):
    logger = logging.getLogger('django')
    code = req.GET.get('code','')
    if not code:
        params = {
            "meta": {
                "code": 400,
                "message": "no code"
            }
        }
        return HttpResponse(json.dumps(params), content_type='application/json')
    wx = Weixin()
    urlResp = wx.get_access_token_info(req, code)
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

    userResp = wx.get_userinfo(req, access_token, openid)
    params = userResp
    return HttpResponse(json.dumps(params), content_type='application/json')