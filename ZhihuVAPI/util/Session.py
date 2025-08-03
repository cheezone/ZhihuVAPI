from .. import config
import os
if config.is_use_chrome_cookies == True and os.name == 'nt':

    import sqlite3
    from win32.win32crypt import CryptUnprotectData
    host = '.zhihu.com'
    if config.cookiepath:  # 使用自己配置的 cookiepath
        cookiepath = config.cookiepath
    if os.path.exists(os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data\Default\Cookies"):  # 使用 Chrome 的 cookiepath
        cookiepath = os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data\Default\Cookies"
    elif os.path.exists(os.environ['LOCALAPPDATA'] + r"\CentBrowser\User Data\Default\Cookies"):  # 使用百分的 cookiepath
        cookiepath = os.environ['LOCALAPPDATA'] + r"\CentBrowser\User Data\Default\Cookies"

    sql = "select host_key,name,encrypted_value from cookies where host_key='%s'" % host
    with sqlite3.connect(cookiepath) as conn:
        cu = conn.cursor()
        cookies = {name: CryptUnprotectData(encrypted_value)[1].decode(
        ) for host_key, name, encrypted_value in cu.execute(sql).fetchall()}
    texts = []
    for k, v in cookies.items():
        # if v.find('"') > -1:
        #     v = v.replace('"', '')
        texts.append(f'{k}={v}')

    # print('Authorization maybe you should get it by yourself')
    hash = ''
    if config.show_cookies_in_loading == True:
        print('默认加载 Chrome 的 Cookies(这可以在 config.py 里面修改):' + '; '.join(texts))
    headers = {
        'Cookie': '; '.join(texts),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/',
        'Origin': 'https://www.zhihu.com/',
        'Content-Type': 'application/json, text/plain, */*',
        'Pragma': 'no-cache',
    }
else:

    # 导入上层的敏感数据
    # import sys
    # sys.path.append("..")
    from .. import config
    hash = config.hash
    headers = config.headers
    """
    位于上层目录的 config.py 内容示例:
    hash = '你的 Hash'
    headers = {
        'Cookie': '_xsrf=...;   z_c0=...'
        'Accept-Encoding': 'gzip',
        'User-Agent': 'ZhihuHybrid com.zhihu.android/Futureve/5.21.2 Mozilla/5.0 (Linux; Android 5.1.1; SM-G925F Build/LMY48Z) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Safari/537.36',
        'x-api-version': '3.0.76',
        'Authorization': '...',
        'x-app-za': 'OS=Android&Release=5.1.1&Model=SM-G925F&VersionName=5.21.2&VersionCode=764&Product=com.zhihu.android&Width=1080&Height=1920&Installer=%E5%BA%94%E7%94%A8%E5%AE%9D-%E5%B9%BF%E5%91%8A&DeviceType=AndroidPhone&Brand=samsung&OperatorType=46000', 'accept': 'application/json, text/plain, */*'
    }
    """
