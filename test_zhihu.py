#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZhihuVAPI 测试脚本
"""

import sys
sys.path.insert(0, '.')

try:
    import ZhihuVAPI as zhihu
    print("✅ ZhihuVAPI 导入成功")
    
    # 测试基本功能
    print("\n📋 测试基本功能:")
    
    # 测试获取用户信息（使用知乎官方账号作为示例）
    try:
        person = zhihu.People('zhihuadmin')
        print(f"✅ 成功创建用户对象: {person.name}")
    except Exception as e:
        print(f"❌ 创建用户对象失败: {e}")
    
    # 测试获取问题
    try:
        question = zhihu.Question('https://www.zhihu.com/question/31343133')
        print(f"✅ 成功创建问题对象: {question.title}")
    except Exception as e:
        print(f"❌ 创建问题对象失败: {e}")
    
    # 测试获取答案
    try:
        answer = zhihu.Answer('https://www.zhihu.com/question/31343133/answer/58763430')
        print(f"✅ 成功创建答案对象")
    except Exception as e:
        print(f"❌ 创建答案对象失败: {e}")
    
    # 测试获取文章
    try:
        article = zhihu.Article('https://zhuanlan.zhihu.com/p/39747259')
        print(f"✅ 成功创建文章对象: {article.title}")
    except Exception as e:
        print(f"❌ 创建文章对象失败: {e}")
    
    # 测试获取专栏
    try:
        column = zhihu.Column('cheezpython')
        print(f"✅ 成功创建专栏对象: {column.title}")
    except Exception as e:
        print(f"❌ 创建专栏对象失败: {e}")
    
    print("\n🎉 基本功能测试完成！")
    print("\n📝 使用说明:")
    print("1. 要使用完整功能，需要配置正确的知乎登录信息")
    print("2. 在 ZhihuVAPI/config.py 中设置正确的 cookies 和 headers")
    print("3. 或者使用 Chrome 浏览器的 cookies（默认配置）")
    
except ImportError as e:
    print(f"❌ 导入失败: {e}")
except Exception as e:
    print(f"❌ 运行出错: {e}")