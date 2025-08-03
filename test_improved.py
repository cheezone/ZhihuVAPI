#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进后的 ZhihuVAPI 测试脚本
使用新的配置和请求头来测试用户信息获取
"""

import sys
sys.path.insert(0, '.')

def test_user_info():
    """测试获取用户信息"""
    try:
        import ZhihuVAPI as zhihu
        print("✅ ZhihuVAPI 导入成功")
        
        # 测试用户URL
        test_users = [
            'https://www.zhihu.com/people/reseted1516084559515',
            'https://www.zhihu.com/people/zhihuadmin',
            'https://www.zhihu.com/people/CheezOne'
        ]
        
        for user_url in test_users:
            print(f"\n🔍 测试用户: {user_url}")
            try:
                user = zhihu.People(user_url)
                print(f"✅ 用户对象创建成功")
                
                # 尝试获取基本信息
                info_attrs = ['name', 'voteup_count', 'favorited_count', 
                             'followers_count', 'question_count', 'answer_count', 
                             'articles_count', 'columns_count']
                
                print("📋 用户信息:")
                for attr in info_attrs:
                    try:
                        value = getattr(user, attr, None)
                        if value is not None:
                            print(f"  {attr}: {value}")
                        else:
                            print(f"  {attr}: 无法获取")
                    except Exception as e:
                        print(f"  {attr}: 获取失败 - {str(e)[:50]}")
                
                # 尝试获取用户的其他属性
                print("\n🔍 用户对象属性:")
                for attr in dir(user):
                    if not attr.startswith('_') and not callable(getattr(user, attr, None)):
                        try:
                            value = getattr(user, attr, None)
                            if value is not None and value != '':
                                print(f"  {attr}: {value}")
                        except:
                            pass
                            
            except Exception as e:
                print(f"❌ 获取用户信息失败: {e}")
                
    except Exception as e:
        print(f"❌ 运行出错: {e}")

def test_api_endpoints():
    """测试API端点"""
    try:
        import ZhihuVAPI as zhihu
        from ZhihuVAPI.util import Session
        
        print("\n🔧 测试API端点:")
        print(f"当前使用的headers:")
        for key, value in Session.headers.items():
            if key.lower() in ['authorization', 'cookie']:
                print(f"  {key}: {value[:50]}..." if len(str(value)) > 50 else f"  {key}: {value}")
            else:
                print(f"  {key}: {value}")
        
        # 测试一些基本的API调用
        test_urls = [
            'https://api.zhihu.com/people/zhihuadmin',
            'https://api.zhihu.com/people/self',
            'https://www.zhihu.com/api/v4/people/zhihuadmin'
        ]
        
        for url in test_urls:
            print(f"\n🌐 测试API: {url}")
            try:
                from ZhihuVAPI.util import zhihu as zhihu_util
                response = zhihu_util.get(url)
                print(f"  状态码: {response.status_code}")
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"  响应数据: {str(data)[:200]}...")
                    except:
                        print(f"  响应内容: {response.text[:200]}...")
                else:
                    print(f"  错误响应: {response.text[:200]}...")
            except Exception as e:
                print(f"  ❌ 请求失败: {e}")
                
    except Exception as e:
        print(f"❌ API测试出错: {e}")

def main():
    print("🚀 改进后的 ZhihuVAPI 测试")
    print("=" * 60)
    
    # 测试用户信息获取
    test_user_info()
    
    # 测试API端点
    test_api_endpoints()
    
    print("\n" + "=" * 60)
    print("🎉 测试完成！")
    print("\n💡 改进说明:")
    print("  • 更新了请求头配置，使用更现代的浏览器User-Agent")
    print("  • 添加了authorization头部，这是成功项目的关键")
    print("  • 改进了错误处理和重试机制")
    print("  • 增加了超时时间和状态码检查")
    print("  • 添加了指数退避重试策略")

if __name__ == "__main__":
    main()