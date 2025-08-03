

# 控制是否输出警告日志,不喜欢的可以改为 False
log_switch = True
# 控制是否输出信息日志,不喜欢的可以改为 False
info_switch = True
# 是否使用 Chrome 的 Cookies
is_use_chrome_cookies = True
# 自定义使用的 Cookie 文件路径
cookiepath = ''
# 用户hash值，用于API调用
hash = ''
# 当 is_use_chrome_cookies = False 时使用的请求头部
headers = {
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
    'Cookie': '_xsrf=...; z_c0=...',
}
# 是否在程序运行时显示 Cookies
show_cookies_in_loading = False
