#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代知乎API客户端
使用最新的反爬虫绕过技术
"""

import requests
import time
import random
import json
from urllib.parse import urlparse, parse_qs

class ModernZhihuAPI:
    def __init__(self):
        self.session = requests.Session()
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        
        # 设置会话默认头部
        self.session.headers.update(self.base_headers)
        
    def get_user_info(self, user_url):
        """获取用户信息"""
        try:
            print(f"🔍 尝试获取用户信息: {user_url}")
            
            # 首先访问用户页面获取必要的cookies
            response = self.session.get(user_url, timeout=10)
            print(f"  页面访问状态码: {response.status_code}")
            
            if response.status_code == 200:
                # 解析页面内容
                content = response.text
                
                # 尝试提取用户信息
                user_info = self._extract_user_info_from_page(content, user_url)
                return user_info
            else:
                print(f"  ❌ 页面访问失败: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"  ❌ 获取用户信息失败: {e}")
            return None
    
    def _extract_user_info_from_page(self, content, user_url):
        """从页面内容中提取用户信息"""
        user_info = {
            'url': user_url,
            'name': None,
            'headline': None,
            'description': None,
            'followers_count': None,
            'following_count': None,
            'answer_count': None,
            'question_count': None,
            'articles_count': None,
            'columns_count': None,
            'voteup_count': None,
            'favorited_count': None,
        }
        
        try:
            # 简单的信息提取（这里可以根据实际页面结构调整）
            if '知乎，让每一次点击都充满意义' in content:
                print("  ⚠️  检测到反爬虫页面，尝试其他方法...")
                return self._try_api_method(user_url)
            
            # 尝试提取用户名
            import re
            name_pattern = r'<title>(.*?)</title>'
            name_match = re.search(name_pattern, content)
            if name_match:
                user_info['name'] = name_match.group(1).replace(' - 知乎', '').replace(' - 知乎用户', '')
            
            print(f"  ✅ 成功提取用户信息")
            print(f"    用户名: {user_info['name']}")
            
            return user_info
            
        except Exception as e:
            print(f"  ❌ 解析页面失败: {e}")
            return user_info
    
    def _try_api_method(self, user_url):
        """尝试使用API方法获取用户信息"""
        try:
            # 从URL中提取用户名
            parsed_url = urlparse(user_url)
            username = parsed_url.path.split('/')[-1]
            
            # 尝试不同的API端点
            api_endpoints = [
                f'https://www.zhihu.com/api/v4/members/{username}',
                f'https://api.zhihu.com/people/{username}',
                f'https://www.zhihu.com/api/v4/people/{username}'
            ]
            
            for endpoint in api_endpoints:
                try:
                    print(f"  🔧 尝试API: {endpoint}")
                    
                    # 添加必要的头部
                    api_headers = self.base_headers.copy()
                    api_headers.update({
                        'Accept': 'application/json, text/plain, */*',
                        'Referer': user_url,
                        'X-Requested-With': 'XMLHttpRequest',
                    })
                    
                    response = self.session.get(endpoint, headers=api_headers, timeout=10)
                    print(f"    API状态码: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            print(f"    ✅ API调用成功")
                            return self._parse_api_response(data, user_url)
                        except json.JSONDecodeError:
                            print(f"    ❌ API返回非JSON数据")
                            continue
                    else:
                        print(f"    ❌ API调用失败: {response.status_code}")
                        continue
                        
                except Exception as e:
                    print(f"    ❌ API请求异常: {e}")
                    continue
            
            print("  ❌ 所有API方法都失败了")
            return None
            
        except Exception as e:
            print(f"  ❌ API方法失败: {e}")
            return None
    
    def _parse_api_response(self, data, user_url):
        """解析API响应数据"""
        user_info = {
            'url': user_url,
            'name': data.get('name'),
            'headline': data.get('headline'),
            'description': data.get('description'),
            'followers_count': data.get('follower_count'),
            'following_count': data.get('following_count'),
            'answer_count': data.get('answer_count'),
            'question_count': data.get('question_count'),
            'articles_count': data.get('articles_count'),
            'columns_count': data.get('columns_count'),
            'voteup_count': data.get('voteup_count'),
            'favorited_count': data.get('favorited_count'),
        }
        
        print(f"  📋 解析到的用户信息:")
        for key, value in user_info.items():
            if value is not None:
                print(f"    {key}: {value}")
        
        return user_info

def main():
    """测试现代知乎API客户端"""
    print("🚀 现代知乎API客户端测试")
    print("=" * 60)
    
    api_client = ModernZhihuAPI()
    
    # 测试用户列表
    test_users = [
        'https://www.zhihu.com/people/reseted1516084559515',
        'https://www.zhihu.com/people/zhihuadmin',
        'https://www.zhihu.com/people/CheezOne'
    ]
    
    for user_url in test_users:
        print(f"\n{'='*40}")
        user_info = api_client.get_user_info(user_url)
        
        if user_info:
            print(f"✅ 成功获取用户信息")
        else:
            print(f"❌ 获取用户信息失败")
        
        # 添加延迟避免请求过于频繁
        time.sleep(random.uniform(1, 3))
    
    print(f"\n{'='*60}")
    print("🎉 测试完成！")
    print("\n💡 现代API客户端特点:")
    print("  • 使用最新的浏览器User-Agent")
    print("  • 添加了必要的安全头部")
    print("  • 实现了多种API端点尝试")
    print("  • 添加了请求延迟和随机化")
    print("  • 改进了错误处理和日志记录")

if __name__ == "__main__":
    main()