#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进的知乎API客户端
基于成功项目的API和配置
"""

import requests
import json
import time
import random
from urllib.parse import urlparse

class ImprovedZhihuAPI:
    def __init__(self):
        self.session = requests.Session()
        
        # 基于成功项目的headers配置
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Host": "www.zhihu.com",
            "Referer": "https://www.zhihu.com/",
            "Origin": "https://www.zhihu.com/",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/json, text/plain, */*",
            "Pragma": "no-cache",
            "Accept-Encoding": "gzip, deflate",
            'Connection': 'close',
            'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
        # 设置会话默认头部
        self.session.headers.update(self.headers)
        
    def get_user_info(self, user_url):
        """获取用户信息 - 使用成功项目的API"""
        try:
            print(f"🔍 尝试获取用户信息: {user_url}")
            
            # 从URL中提取用户名
            parsed_url = urlparse(user_url)
            username = parsed_url.path.split('/')[-1]
            
            # 使用成功项目的API端点
            api_url = f'https://www.zhihu.com/api/v4/members/{username}?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
            
            print(f"  🔧 使用API: {api_url}")
            
            response = self.session.get(api_url, timeout=35)
            print(f"  状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  ✅ API调用成功")
                    return self._parse_user_data(data, user_url)
                except json.JSONDecodeError as e:
                    print(f"  ❌ JSON解析失败: {e}")
                    print(f"  响应内容: {response.text[:200]}...")
                    return None
            else:
                print(f"  ❌ API调用失败: {response.status_code}")
                print(f"  错误响应: {response.text[:200]}...")
                return None
                
        except Exception as e:
            print(f"  ❌ 获取用户信息失败: {e}")
            return None
    
    def _parse_user_data(self, data, user_url):
        """解析用户数据"""
        user_info = {
            'url': user_url,
            'name': data.get('name'),
            'headline': data.get('headline'),
            'description': data.get('description'),
            'gender': data.get('gender'),
            'follower_count': data.get('follower_count'),
            'following_count': data.get('following_count'),
            'answer_count': data.get('answer_count'),
            'question_count': data.get('question_count'),
            'articles_count': data.get('articles_count'),
            'pins_count': data.get('pins_count'),
            'voteup_count': data.get('voteup_count'),
            'thanked_count': data.get('thanked_count'),
            'favorited_count': data.get('favorited_count'),
            'url_token': data.get('url_token'),
            'type': data.get('type'),
            'account_status': data.get('account_status'),
            'is_active': data.get('is_active'),
            'allow_message': data.get('allow_message'),
        }
        
        print(f"  📋 解析到的用户信息:")
        for key, value in user_info.items():
            if value is not None:
                print(f"    {key}: {value}")
        
        return user_info
    
    def get_user_followers(self, username, offset=0, limit=20):
        """获取用户的粉丝列表"""
        try:
            api_url = f'https://www.zhihu.com/api/v4/members/{username}/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={offset}&limit={limit}'
            
            response = self.session.get(api_url, timeout=35)
            
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"获取粉丝列表失败: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"获取粉丝列表异常: {e}")
            return None
    
    def get_user_following(self, username, offset=0, limit=20):
        """获取用户的关注列表"""
        try:
            api_url = f'https://www.zhihu.com/api/v4/members/{username}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={offset}&limit={limit}'
            
            response = self.session.get(api_url, timeout=35)
            
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"获取关注列表失败: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"获取关注列表异常: {e}")
            return None

def main():
    """测试改进的知乎API客户端"""
    print("🚀 改进的知乎API客户端测试")
    print("=" * 60)
    
    api_client = ImprovedZhihuAPI()
    
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
            
            # 如果获取成功，尝试获取粉丝列表
            if user_info.get('url_token'):
                print(f"\n🔍 尝试获取粉丝列表...")
                followers = api_client.get_user_followers(user_info['url_token'], limit=5)
                if followers:
                    print(f"✅ 成功获取粉丝列表，共 {followers.get('paging', {}).get('totals', 0)} 个粉丝")
                else:
                    print(f"❌ 获取粉丝列表失败")
        else:
            print(f"❌ 获取用户信息失败")
        
        # 添加延迟避免请求过于频繁
        time.sleep(random.uniform(1, 3))
    
    print(f"\n{'='*60}")
    print("🎉 测试完成！")
    print("\n💡 改进说明:")
    print("  • 使用了成功项目的API端点: /api/v4/members/")
    print("  • 采用了正确的headers配置")
    print("  • 包含了完整的include参数")
    print("  • 实现了粉丝和关注列表获取")
    print("  • 添加了详细的错误处理")

if __name__ == "__main__":
    main()