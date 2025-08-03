#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试获取特定用户信息
"""

import sys
sys.path.insert(0, '.')

try:
    import ZhihuVAPI as zhihu
    print("✅ ZhihuVAPI 导入成功")
    
    # 测试获取特定用户信息
    user_url = 'https://www.zhihu.com/people/reseted1516084559515'
    print(f"\n🔍 尝试获取用户信息: {user_url}")
    
    try:
        user = zhihu.People(user_url)
        print(f"✅ 用户对象创建成功")
        
        # 尝试获取用户基本信息
        print("\n📋 用户信息:")
        try:
            print(f"用户名: {user.name}")
        except:
            print("用户名: 无法获取")
            
        try:
            print(f"赞同数: {user.voteup_count}")
        except:
            print("赞同数: 无法获取")
            
        try:
            print(f"收藏数: {user.favorited_count}")
        except:
            print("收藏数: 无法获取")
            
        try:
            print(f"粉丝数: {user.followers_count}")
        except:
            print("粉丝数: 无法获取")
            
        try:
            print(f"问题数: {user.question_count}")
        except:
            print("问题数: 无法获取")
            
        try:
            print(f"答案数: {user.answer_count}")
        except:
            print("答案数: 无法获取")
            
        try:
            print(f"文章数: {user.articles_count}")
        except:
            print("文章数: 无法获取")
            
        try:
            print(f"专栏数: {user.columns_count}")
        except:
            print("专栏数: 无法获取")
            
        # 尝试获取用户的其他属性
        print("\n🔍 用户对象属性:")
        for attr in dir(user):
            if not attr.startswith('_'):
                try:
                    value = getattr(user, attr)
                    if not callable(value):
                        print(f"{attr}: {value}")
                except:
                    pass
                    
    except Exception as e:
        print(f"❌ 获取用户信息失败: {e}")
        
except Exception as e:
    print(f"❌ 运行出错: {e}")