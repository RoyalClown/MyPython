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
        """登陆.

        :param str email: 邮箱
        :param str password: 密码
        :param str captcha: 验证码, 默认为None，表示不提交验证码
        :return:
            ======== ======== ============== ====================
            元素序号 元素类型 意义           说明
            ======== ======== ============== ====================
            0        int      是否成功       0为成功，1为失败
            1        str      失败原因       登录成功则为空字符串
            2        str       cookies字符串 登录失败则为空字符串
            ======== ======== ============== ====================

        :rtype: (int, str, str)
        """
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
        """使用cookies文件或字符串登录

        :param str cookies:
            ============== ===========================
            参数形式       作用
            ============== ===========================
            文件名         将文件内容作为cookies字符串
            cookies 字符串  直接提供cookies字符串
            ============== ===========================
        :return: 无
        :rtype: None
        """
        if os.path.isfile(cookies):
            with open(cookies) as f:
                cookies = f.read()
        cookies_dict = json.loads(cookies)
        self._session.cookies.update(cookies_dict)

    def login_in_terminal(self, need_captcha=False, use_getpass=True):
        """不使用cookies，在终端中根据提示登陆

        :param bool need_captcha: 是否要求输入验证码，如果登录失败请设为 True
        :param bool use_getpass: 是否使用安全模式输入密码，默认为 True，
            如果在某些 Windows IDE 中无法正常输入密码，请把此参数设置为 False 试试
        :return: 如果成功返回cookies字符串
        :rtype: str
        """
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
        """在终端中执行登录流程，将 cookies 存放在文件中以便后续使用

        :param str file: 文件名
        :param bool need_captcha: 登录过程中是否使用验证码， 默认为 False
        :param bool use_getpass: 是否使用安全模式输入密码，默认为 True，
            如果在某些 Windows IDE 中无法正常输入密码，请把此参数设置为 False 试试
        :return:
        """
        cookies_str = self.login_in_terminal(need_captcha, use_getpass)
        if cookies_str:
            with open(file, 'w') as f:
                f.write(cookies_str)
            print('cookies file created.')
        else:
            print('can\'t create cookies.')

    # ===== network staff =====

    def set_proxy(self, proxy):
        """设置代理

        :param str proxy: 使用 "http://example.com:port" 的形式
        :return: 无
        :rtype: None

        :说明:
            由于一个 :class:`.Client` 对象和它创建出来的其他对象共用
            一个Session，所以调用这个方法也会将所有生成出的类设置上代理。
        """
        self._session.proxies.update({'http': proxy})

    def set_proxy_pool(self, proxies, auth=None, https=True):
        """设置代理池

        :param proxies: proxy列表, 形如 ``["ip1:port1", "ip2:port2"]``
        :param auth: 如果代理需要验证身份, 通过这个参数提供, 比如
        :param https: 默认为 True, 传入 False 则不设置 https 代理
        .. code-block:: python

              from requests.auth import HTTPProxyAuth
              auth = HTTPProxyAuth('laike9m', '123')
        :说明:
             每次 GET/POST 请求会随机选择列表中的代理
        """
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
