from .. import config
if config.is_use_chrome_cookies == True:

    import os
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
        'Accept-Encoding': 'gzip',
        # 'User-Agent': 'com.zhihu.android/Futureve/5.21.2 Mozilla/5.0 (Linux; Android 5.1.1; SM-G925F Build/LMY48Z) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Safari/537.36',
        'User-Agent': 'ZhihuHybrid com.zhihu.android/Futureve/5.21.2 Mozilla/5.0 (Linux; Android 5.1.1; SM-G925F Build/LMY48Z) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Safari/537.36',
        # 是个坑点
        # 'Authorization': 'Bearer 2.1nT3nAgAAAAAAQCTkYHbtDQwAAABgAlVN5OR7WwDipjTIOQZzMdBwDlgXIdlLs0_Wsw',
        'x-api-version': '3.0.76',
        'x-app-version': '5.21.2',
        'x-app-flavor': 'yybgg',
        'x-app-build': 'release',
        'x-network-type': 'WiFi',
        # 'X-SUGER':  'SU1FST04NjQ1Mzc3NDIxMzI3MTE7QU5EUk9JRF9JRD05MDE3MDQ0MTc0Mjc1ODE0',
        # 'X-ZST-82': '1.0AHDn446V-w0MAAAASwUAADEuMGbAX1sAAAAAOq9apOGfzFKL1bLw2B6sBVAhm4M=',
        # 'x-udid': 'AEAk5GB27Q1LBUlfpLUtrEBLk8F7KE62dbU=',
        'x-requested-with': 'Fetch',
        'x-app-za': 'OS=Android&Release=5.1.1&Model=SM-G925F&VersionName=5.21.2&VersionCode=764&Product=com.zhihu.android&Width=1080&Height=1920&Installer=%E5%BA%94%E7%94%A8%E5%AE%9D-%E5%B9%BF%E5%91%8A&DeviceType=AndroidPhone&Brand=samsung&OperatorType=46000', 'accept': 'application/json, text/plain, */*'

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
