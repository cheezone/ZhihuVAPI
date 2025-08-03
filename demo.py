#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZhihuVAPI 演示脚本
展示如何使用 ZhihuVAPI 获取知乎数据
"""

import sys
sys.path.insert(0, '.')

def main():
    print("🚀 ZhihuVAPI 演示")
    print("=" * 50)
    
    try:
        import ZhihuVAPI as zhihu
        print("✅ 模块导入成功")
        
        print("\n📋 功能演示:")
        
        # 演示1：基本对象创建
        print("\n1️⃣ 基本对象创建演示:")
        
        # 用户对象
        try:
            user = zhihu.People('zhihuadmin')
            print(f"   ✅ 用户对象创建成功")
        except Exception as e:
            print(f"   ❌ 用户对象创建失败: {str(e)[:50]}...")
        
        # 问题对象
        try:
            question = zhihu.Question('https://www.zhihu.com/question/31343133')
            print(f"   ✅ 问题对象创建成功")
        except Exception as e:
            print(f"   ❌ 问题对象创建失败: {str(e)[:50]}...")
        
        # 答案对象
        try:
            answer = zhihu.Answer('https://www.zhihu.com/question/31343133/answer/58763430')
            print(f"   ✅ 答案对象创建成功")
        except Exception as e:
            print(f"   ❌ 答案对象创建失败: {str(e)[:50]}...")
        
        # 文章对象
        try:
            article = zhihu.Article('https://zhuanlan.zhihu.com/p/39747259')
            print(f"   ✅ 文章对象创建成功")
        except Exception as e:
            print(f"   ❌ 文章对象创建失败: {str(e)[:50]}...")
        
        # 专栏对象
        try:
            column = zhihu.Column('cheezpython')
            print(f"   ✅ 专栏对象创建成功")
        except Exception as e:
            print(f"   ❌ 专栏对象创建失败: {str(e)[:50]}...")
        
        # 演示2：API功能说明
        print("\n2️⃣ API功能说明:")
        print("   📝 获取用户信息: zhihu.People('用户名')")
        print("   📝 获取问题信息: zhihu.Question('问题URL')")
        print("   📝 获取答案信息: zhihu.Answer('答案URL')")
        print("   📝 获取文章信息: zhihu.Article('文章URL')")
        print("   📝 获取专栏信息: zhihu.Column('专栏URL')")
        print("   📝 获取收藏夹: zhihu.Collection('收藏夹URL')")
        
        # 演示3：高级功能
        print("\n3️⃣ 高级功能:")
        print("   🔍 获取用户答案列表: user.answers(count=5)")
        print("   🔍 获取用户粉丝列表: user.followers(count=10)")
        print("   🔍 获取问题答案列表: question.answers(count=5)")
        print("   🔍 获取答案点赞用户: answer.voters(count=5)")
        print("   🔍 获取文章点赞用户: article.voters(count=5)")
        
        # 演示4：交互功能
        print("\n4️⃣ 交互功能:")
        print("   👍 点赞答案: answer.vote()")
        print("   👎 反对答案: answer.down()")
        print("   ❤️ 感谢答案: answer.thank()")
        print("   👥 关注用户: user.follow()")
        print("   💬 发送私信: user.send('消息内容')")
        
        # 演示5：配置说明
        print("\n5️⃣ 配置说明:")
        print("   ⚙️ 配置文件: ZhihuVAPI/config.py")
        print("   🔐 登录方式: Chrome cookies 或手动配置")
        print("   📊 日志控制: log_switch 和 info_switch")
        
        print("\n" + "=" * 50)
        print("🎉 演示完成！")
        print("\n💡 提示:")
        print("   • 要使用完整功能，请配置正确的知乎登录信息")
        print("   • 查看 使用说明.md 了解详细配置方法")
        print("   • 遵守知乎使用条款，合理使用API")
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保已安装 requests 库: pip install requests")
    except Exception as e:
        print(f"❌ 运行出错: {e}")

if __name__ == "__main__":
    main()