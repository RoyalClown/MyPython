import getpass
import json
import os
import time
from urllib.parse import urlencode

import requests

from .Constant import *


class NameClient:
    """客户端类，内部维护了自己专用的网络会话，可用cookies或账号密码登录."""

    def __init__(self, cookies=None):
        """创建客户端类实例.

        :param str cookies: 见 :meth:`.login_with_cookies` 中 ``cookies`` 参数
        :return: 客户端对象
        :rtype: Client
        """
        self._session = requests.Session()
        self._session.headers.update(Default_Header)
        self.proxies = None
        if cookies is not None:
            assert isinstance(cookies, str)
            self.login_with_cookies(cookies)

    # ===== login staff =====

    @staticmethod
    def _get_captcha_url():
        params = {
            'r': str(int(time.time() * 1000)),
            'type': 'login',
        }
        return Captcha_Url + '?' + urlencode(params)

    def get_captcha(self):
        """获取验证码数据。

        :return: 验证码图片数据。
        :rtype: bytes
        """
        self._session.get(URL)
        r = self._session.get(self._get_captcha_url())
        return r.content

    def login(self, email, password, captcha=None):

        data = {'email': email, 'password': password,
                'remember_me': 'true'}
        if captcha is not None:
            data['captcha'] = captcha
        r = self._session.post(Login_Url, data=data)
        j = r.json()
        code = int(j['r'])
        message = j['msg']
        cookies_str = json.dumps(self._session.cookies.get_dict()) \
            if code == 0 else ''
        return code, message, cookies_str

    def login_with_cookies(self, cookies):

        if os.path.isfile(cookies):
            with open(cookies) as f:
                cookies = f.read()
        cookies_dict = json.loads(cookies)
        self._session.cookies.update(cookies_dict)

    def login_in_terminal(self, need_captcha=False, use_getpass=True):

        print('====== login =====')

        email = input('email: ')
        if use_getpass:
            password = getpass.getpass('password: ')
        else:
            password = input("password: ")

        if need_captcha:
            captcha_data = self.get_captcha()
            with open('captcha.gif', 'wb') as f:
                f.write(captcha_data)

            print('please check captcha.gif for captcha')
            captcha = input('captcha: ')
            os.remove('captcha.gif')
        else:
            captcha = None

        print('====== logging.... =====')

        code, msg, cookies = self.login(email, password, captcha)

        if code == 0:
            print('login successfully')
        else:
            print('login failed, reason: {0}'.format(msg))

        return cookies

    def create_cookies(self, file, need_captcha=False, use_getpass=True):

        cookies_str = self.login_in_terminal(need_captcha, use_getpass)
        if cookies_str:
            with open(file, 'w') as f:
                f.write(cookies_str)
            print('cookies file created.')
        else:
            print('can\'t create cookies.')

    # ===== network staff =====

    def set_proxy(self, proxy):

        self._session.proxies.update({'http': proxy})

    def set_proxy_pool(self, proxies, auth=None, https=True):

        from random import choice

        if https:
            self.proxies = [{'http': p, 'https': p} for p in proxies]
        else:
            self.proxies = [{'http': p} for p in proxies]

        def get_with_random_proxy(url, **kwargs):
            proxy = choice(self.proxies)
            kwargs['proxies'] = proxy
            if auth:
                kwargs['auth'] = auth
            return self._session.original_get(url, **kwargs)

        def post_with_random_proxy(url, *args, **kwargs):
            proxy = choice(self.proxies)
            kwargs['proxies'] = proxy
            if auth:
                kwargs['auth'] = auth
            return self._session.original_post(url, *args, **kwargs)

        self._session.original_get = self._session.get
        self._session.get = get_with_random_proxy
        self._session.original_post = self._session.post
        self._session.post = post_with_random_proxy

    def remove_proxy_pool(self):
        """
        移除代理池
        """
        self.proxies = None
        self._session.original_get = self._session.get
        self._session.original_post = self._session.post
        del self._session.original_get
        del self._session.original_post
