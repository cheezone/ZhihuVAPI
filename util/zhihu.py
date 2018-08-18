import re
import requests
import urllib3
from . import urls
import json as json_moudle
from . import Session
from .. import config
# ============================
# ====  配置
# ============================

# 下面这两条禁用了 SSL 验证和警告,当你不需要抓包的时候注释掉他们
verify = False
urllib3.disable_warnings()


def log(*arg):
    '''根据 log_switch参数输出日志，并解决编码问题'''
    if config.log_switch == True:
        arg = list(map(lambda x: ('日志：' + x.encode('gbk', 'ignore').decode('gbk') if type(x) == type('') else x), arg))
        print(*arg)


def info(*arg):
    '''根据 info_switch 参数输出日志，并解决编码问题'''
    if config.info_switch == True:
        arg = list(map(lambda x: ('信息：' + x.encode('gbk', 'ignore').decode('gbk') if type(x) == type('') else x), arg))
        print(*arg)


def test(object, test_type, value):
    '''
    用于测试属性
    '''
    if value.__class__.__name__ != 'str':
        return False
    if test_type == 'id':
        if object.type_name == '用户':
            return bool(re.fullmatch(r'[\da-zA-Z]{32}', value))
        elif object.type_name == '问题':
            # 19550224 开始
            return bool(re.fullmatch(r'\d{8,12}', value))
        elif object.type_name == '答案':
            return bool(re.fullmatch(r'\d{8,12}', value))
        elif object.type_name == 'Live':
            return bool(re.fullmatch(r'\d{18}', value))
        elif object.type_name == '文章':
            return bool(re.fullmatch(r'\d{8,12}', value))
        elif object.type_name == '专栏':
            return bool(re.fullmatch(r'[\da-zA-Z-_]{1,}', value))
        elif object.type_name == '想法':
            return bool(re.fullmatch(r'[\d]{1,}', value))
    elif test_type == 'token':
        if object.type_name == '用户':
            return bool(re.fullmatch(r'[\da-zA-Z-_]{1,}', value))

    return False


def need_login(inner_func):
    def wraper(*args, **kwargs):
        # TODO:判断是否登录
        inner_func(*args, **kwargs)
    return wraper


def get(url, *arg):
    """
    对 Requests GET 请求的包装,加上了知乎需要的 Headers。
    """
    try:
        r = requests.get(url, headers=Session.headers,
                         verify=verify, timeout=3, *arg)
        r.encoding = 'utf-8'  # 强制按 UTF-8 来解析
        return r
    except requests.exceptions.ProxyError:
        log(f'访问{url}时出错,检查你的代理')
    except:
        try:
            r = requests.get(url, headers=Session.headers,
                             verify=verify, timeout=3, *arg)
            r.encoding = 'gbk'  # 强制按 GBK 来解析
            return r
        except Exception as e:
            raise e
            log(f'实在没办法了,按 GBK 来解析也没有用,我也不知道发生什么事:{url}')


def error(JSON, url='', h=''):
    if JSON.get('code') == 100:
        print('错误代码 100:检查 Headers 里的 Authorization')
    else:
        print(f'错误代码({JSON.get("code")})： {JSON.get("message").encode("gbk", "ignore").decode( "gbk")}({url}) ')


def post(url, data, *arg):
    """
    对 Requests POST 请求的包装,加上了知乎需要的 Headers。
    """
    try:
        r = requests.post(url, headers=Session.headers,
                          verify=verify, timeout=3, data=data, *arg)
        r.encoding = 'utf-8'  # 强制按 UTF-8 来解析
        return r
    except requests.exceptions.ProxyError:
        log(f'访问{url}时出错,检查你的代理')
    except:
        try:
            r = requests.get(url, headers=Session.headers,
                             verify=verify, timeout=3, *arg)
            r.encoding = 'gbk'  # 强制按 GBK 来解析
            return r
        except:
            log(f'实在没办法了,按 GBK 来解析也没有用,我也不知道发生什么事:{url}')


def json(url, *arg):
    """
    自动将 GET 请求转换为 JSON
    """
    try:
        text = get(url, *arg).text
        responseJSON = json_moudle.loads(text)
        if 'error' in responseJSON:
            error(responseJSON['error'], url, Session.headers)

        return responseJSON
    except json_moudle.decoder.JSONDecodeError as e:
        log(f'JSON 解析错误,请检查知乎 API 的 URL 是否变化,当前 URL 为:{url},内容为:{text}')


def jsonp(url, data={}, *arg):
    """
    自动将 POST 请求转换为 JSON
    """
    try:
        text = post(url, data, *arg).text
        responseJSON = json_moudle.loads(text)
        if 'error' in responseJSON:
            error(responseJSON['error'], url, Session.headers)
        return responseJSON
    except json_moudle.decoder.JSONDecodeError as e:
        log(f'JSON 解析错误,请检查知乎 API 的 URL 是否变化,当前 URL 为:{url},内容为:{text}')


def jsonput(url, data={}, *arg):
    """
    自动将 PUT 请求转换为 JSON
    """
    try:
        return json_moudle.loads(requests.put(url, *arg, data=data, headers=Session.headers,
                                              verify=verify, timeout=3).text)
    except json_moudle.decoder.JSONDecodeError as e:
        log(f'JSON 解析错误,请检查知乎 API 的 URL 是否变化,当前 URL 为:{url}')


def jsond(url, *arg):
    """
    自动将 DELETE 请求转换为 JSON
    """
    try:
        return json_moudle.loads(requests.delete(url, headers=Session.headers,
                                                 verify=verify, timeout=3, *arg).text)
    except json_moudle.decoder.JSONDecodeError as e:
        log(f'JSON 解析错误,请检查知乎 API 的 URL 是否变化,当前 URL 为:{url}')


def iter_factory(url_function_name, method=json):
    """返回一个用deal遍历obj的生成器

    Arguments:
        action_name {[string]} -- [动作的名字]
        deal_function {[function]} -- [处理遍历到的数据的函数]
        method {[type]} -- [处理 URL 的函数] (default: {json})
        method_arg {[type]} -- [剩下要传给method的参数]

    Returns:
        [iter] -- [生成器]
    """
    def decorate(deal_function):  # 一个装饰器
        import functools

        doc = deal_function.__doc__

        # @wrap
        @property
        def warpper(self, **kargs):
            def info_collect_function(responseJSON: dict):
                for k, v in responseJSON.items():
                    if k not in ['data', 'paging']:
                        setattr(self, k, v)

            # @log_attr(deal_function.__doc__)
            def iter_function(count=-1, start=1, page=-1, **kwargs):
                import time
                # 根据页数或者开始位置得到偏移值
                if count == -1:
                    offset = 0
                elif page > 0:
                    offset = (page - 1) * 10
                else:
                    offset = int(start / 10) * 10
                data = {}
                data.update({'type_name': self.type_name})
                if self.__class__.__name__ == 'People|':
                    data.update({'name': self.name})
                elif re.match(r"Question|Column|Collection|Topic", self.__class__.__name__):
                    data.update({'name': self.title})
                elif re.match(r"Answer|Article|Comment", self.__class__.__name__):
                    data.update({'name': self.author.name})
                if doc:
                    log(doc.format(**data))
                # 获取 JSON
                responseJSON = method(urls.urls(self, url_function_name)(offset=offset, **kwargs))
                info_collect_function(responseJSON)
                i = offset + 1  # 当前指针(从1开始)
                diff = start - i  # 指针与想要开始的位置的差值
                i_page = 1
                while True:
                    for v in responseJSON['data']:
                        # log(f'i:{i};start:{start};i-start:{i-start}')
                        if diff > 0:  # diff=0时就到达了start
                            diff -= 1
                        elif count == -1:  # 处理没有数量限制的情况
                            yield deal_function(v)
                        elif i - start < count:  # 处理有数量限制的情况
                            yield deal_function(v)
                        else:
                            return None
                        i += 1
                    else:
                        if responseJSON['paging']['is_end'] == False:
                            time.sleep(0.5)
                            responseJSON = method(responseJSON['paging']['next'])
                            info_collect_function(responseJSON)

                            if 'error' in responseJSON:
                                return None
                            i_page += 1
                            # 当指定的页数结束后
                            if i_page == page + 1:
                                return None
                        else:
                            return None
            return iter_function
        return warpper
    return decorate


def log_attr(func):
    '''根据函数的doc-string输出日志'''
    doc = func.__doc__
    if func.__class__.__name__ == 'property':
        @property
        def warpper(self, *args, **kwargs):
            data = {}
            data.update({'type_name': self.type_name})
            if self.__class__.__name__ == 'People':
                data.update({'name': self.name})
            elif re.match(r"Question|Column|Collection|Topic", self.__class__.__name__):
                data.update({'name': self.title})
            elif re.match(r"Answer|Article", self.__class__.__name__):
                data.update({'name': self.author.name})

            log(doc.format(**data))
            return func.__get__.__call__(self, *args, **kwargs)
        return warpper
    elif func.__class__.__name__ == 'function':
        def warpper(self, *args, **kwargs):
            data = {}
            data.update({'type_name': self.type_name})
            if self.__class__.__name__ == 'People':
                data.update({'name': self.name})
            elif re.match(r"Question|Column|Collection|Topic", self.__class__.__name__):
                data.update({'name': self.title})
            elif re.match(r"Answer|Article", self.__class__.__name__):
                data.update({'name': self.author.name})
            log(doc.format(**data))
            return func(self, *args, **kwargs)
        return warpper
