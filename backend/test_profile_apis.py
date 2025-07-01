#!/usr/bin/env python3
"""
测试用户个人资料API
"""

import requests
import json

def test_profile_apis():
    """测试个人资料相关API"""
    print("🧪 测试用户个人资料API...")
    
    base_url = "http://localhost:8000/api/v1"
    
    try:
        # 1. 学生登录
        print("\n1. 学生登录...")
        login_response = requests.post(
            f"{base_url}/auth/login",
            json={
                "username": "student1",
                "password": "123456",
                "remember_me": False
            }
        )
        
        if login_response.status_code != 200:
            print(f"❌ 登录失败: {login_response.text}")
            return
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ 登录成功")
        
        # 2. 获取用户基本信息
        print("\n2. 获取用户基本信息...")
        profile_response = requests.get(
            f"{base_url}/users/profile",
            headers=headers
        )
        
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            print("✅ 获取用户信息成功")
            print(f"   用户名: {profile_data.get('username')}")
            print(f"   邮箱: {profile_data.get('email')}")
            print(f"   姓名: {profile_data.get('full_name')}")
            print(f"   手机: {profile_data.get('phone')}")
        else:
            print(f"❌ 获取用户信息失败: {profile_response.text}")
        
        # 3. 获取学生档案
        print("\n3. 获取学生档案...")
        student_profile_response = requests.get(
            f"{base_url}/users/student-profile",
            headers=headers
        )
        
        if student_profile_response.status_code == 200:
            student_data = student_profile_response.json()
            print("✅ 获取学生档案成功")
            print(f"   学号: {student_data.get('student_id')}")
            print(f"   学校: {student_data.get('school')}")
            print(f"   学院: {student_data.get('college')}")
            print(f"   专业: {student_data.get('major')}")
        elif student_profile_response.status_code == 404:
            print("ℹ️  学生档案不存在，这是正常的")
        else:
            print(f"❌ 获取学生档案失败: {student_profile_response.text}")
        
        # 4. 更新用户基本信息
        print("\n4. 更新用户基本信息...")
        update_data = {
            "full_name": "测试学生",
            "phone": "13800138000"
        }
        
        update_response = requests.put(
            f"{base_url}/users/profile",
            headers=headers,
            json=update_data
        )
        
        if update_response.status_code == 200:
            updated_data = update_response.json()
            print("✅ 更新用户信息成功")
            print(f"   新姓名: {updated_data.get('full_name')}")
            print(f"   新手机: {updated_data.get('phone')}")
        else:
            print(f"❌ 更新用户信息失败: {update_response.text}")
        
        # 5. 创建/更新学生档案
        print("\n5. 创建/更新学生档案...")
        student_data = {
            "student_id": "2021012345",
            "school": "清华大学",
            "college": "计算机科学与技术学院",
            "major": "计算机科学与技术",
            "grade": "2021级",
            "class_name": "计科1班"
        }
        
        student_update_response = requests.put(
            f"{base_url}/users/student-profile",
            headers=headers,
            json=student_data
        )
        
        if student_update_response.status_code == 200:
            student_result = student_update_response.json()
            print("✅ 更新学生档案成功")
            print(f"   学号: {student_result.get('student_id')}")
            print(f"   学校: {student_result.get('school')}")
            print(f"   学院: {student_result.get('college')}")
        else:
            print(f"❌ 更新学生档案失败: {student_update_response.text}")
        
        # 6. 测试密码修改
        print("\n6. 测试密码修改...")
        password_data = {
            "current_password": "123456",
            "new_password": "newpass123",
            "confirm_password": "newpass123"
        }
        
        password_response = requests.post(
            f"{base_url}/auth/change-password",
            headers=headers,
            json=password_data
        )
        
        if password_response.status_code == 200:
            print("✅ 密码修改成功")
            
            # 7. 用新密码重新登录验证
            print("\n7. 用新密码重新登录验证...")
            new_login_response = requests.post(
                f"{base_url}/auth/login",
                json={
                    "username": "student1",
                    "password": "newpass123",
                    "remember_me": False
                }
            )
            
            if new_login_response.status_code == 200:
                print("✅ 新密码登录成功")
                
                # 8. 恢复原密码
                print("\n8. 恢复原密码...")
                new_token = new_login_response.json()["access_token"]
                new_headers = {"Authorization": f"Bearer {new_token}"}
                
                restore_password_response = requests.post(
                    f"{base_url}/auth/change-password",
                    headers=new_headers,
                    json={
                        "current_password": "newpass123",
                        "new_password": "123456",
                        "confirm_password": "123456"
                    }
                )
                
                if restore_password_response.status_code == 200:
                    print("✅ 密码已恢复")
                else:
                    print(f"❌ 恢复密码失败: {restore_password_response.text}")
            else:
                print(f"❌ 新密码登录失败: {new_login_response.text}")
        else:
            print(f"❌ 密码修改失败: {password_response.text}")
        
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {e}")


def test_teacher_profile():
    """测试教师个人资料API"""
    print("\n\n🧪 测试教师个人资料API...")
    
    base_url = "http://localhost:8000/api/v1"
    
    try:
        # 教师登录
        print("\n1. 教师登录...")
        login_response = requests.post(
            f"{base_url}/auth/login",
            json={
                "username": "teacher1",
                "password": "123456",
                "remember_me": False
            }
        )
        
        if login_response.status_code != 200:
            print(f"❌ 教师登录失败: {login_response.text}")
            return
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ 教师登录成功")
        
        # 获取教师档案
        print("\n2. 获取教师档案...")
        teacher_profile_response = requests.get(
            f"{base_url}/users/teacher-profile",
            headers=headers
        )
        
        if teacher_profile_response.status_code == 200:
            teacher_data = teacher_profile_response.json()
            print("✅ 获取教师档案成功")
            print(f"   工号: {teacher_data.get('teacher_id')}")
            print(f"   部门: {teacher_data.get('department')}")
            print(f"   职称: {teacher_data.get('title')}")
        elif teacher_profile_response.status_code == 404:
            print("ℹ️  教师档案不存在")
        else:
            print(f"❌ 获取教师档案失败: {teacher_profile_response.text}")
        
    except Exception as e:
        print(f"❌ 教师测试过程中出现异常: {e}")


def main():
    """主函数"""
    print("🚀 用户个人资料API测试")
    print("=" * 60)
    
    # 测试学生个人资料API
    test_profile_apis()
    
    # 测试教师个人资料API
    test_teacher_profile()
    
    print("\n" + "=" * 60)
    print("📋 测试总结:")
    print("1. 用户基本信息 API: /users/profile")
    print("2. 学生档案 API: /users/student-profile")
    print("3. 教师档案 API: /users/teacher-profile")
    print("4. 密码修改 API: /auth/change-password")
    print("\n💡 如果所有测试通过，前端个人资料页面应该能正常工作")


if __name__ == "__main__":
    main()
