

# 控制是否输出警告日志,不喜欢的可以改为 False
log_switch = True
# 控制是否输出信息日志,不喜欢的可以改为 False
info_switch = True
# 是否使用 Chrome 的 Cookies
is_use_chrome_cookies = True
# 自定义使用的 Cookie 文件路径
cookiepath = ''
# 当 is_use_chrome_cookies = False 时使用的请求头部
headers = {
    'Cookie': '_xsrf=...;   z_c0=...',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'ZhihuHybrid com.zhihu.android/Futureve/5.21.2 Mozilla/5.0 (Linux; Android 5.1.1; SM-G925F Build/LMY48Z) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Safari/537.36',
    'x-api-version': '3.0.76',
    'Authorization': '...',
    'x-app-za': 'OS=Android&Release=5.1.1&Model=SM-G925F&VersionName=5.21.2&VersionCode=764&Product=com.zhihu.android&Width=1080&Height=1920&Installer=%E5%BA%94%E7%94%A8%E5%AE%9D-%E5%B9%BF%E5%91%8A&DeviceType=AndroidPhone&Brand=samsung&OperatorType=46000', 'accept': 'application/json, text/plain, */*'
}
# 是否在程序运行时显示 Cookies
show_cookies_in_loading = False
