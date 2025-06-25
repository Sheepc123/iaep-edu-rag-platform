"""
简单的课程注册数据创建脚本
"""
import sqlite3
import os
from datetime import datetime, timedelta


def create_enrollment_data():
    """创建课程注册测试数据"""
    
    # 数据库文件路径
    db_path = os.path.join(os.path.dirname(__file__), "database", "data", "education_platform.db")
    
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        return
    
    print(f"✅ 连接数据库: {db_path}")
    
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查现有数据
        print("\n=== 检查现有数据 ===")
        
        # 检查用户
        cursor.execute("SELECT id, username, role FROM users WHERE role = 'student' LIMIT 1")
        student = cursor.fetchone()
        
        if not student:
            print("❌ 未找到学生用户")
            return
        
        student_id = student[0]
        print(f"✅ 找到学生用户: {student[1]} (ID: {student_id})")
        
        # 检查课程
        cursor.execute("SELECT id, title FROM courses WHERE is_published = 1 LIMIT 5")
        courses = cursor.fetchall()
        
        if not courses:
            print("❌ 未找到已发布的课程")
            return
        
        print(f"✅ 找到 {len(courses)} 门已发布课程")
        
        # 检查现有注册记录
        cursor.execute("SELECT COUNT(*) FROM course_enrollments WHERE student_id = ?", (student_id,))
        existing_count = cursor.fetchone()[0]
        print(f"ℹ️  学生已注册 {existing_count} 门课程")
        
        # 为学生注册前3门课程
        enrolled_count = 0
        for i, course in enumerate(courses[:3]):
            course_id, course_title = course
            
            # 检查是否已经注册
            cursor.execute("""
                SELECT id FROM course_enrollments 
                WHERE student_id = ? AND course_id = ?
            """, (student_id, course_id))
            
            if cursor.fetchone():
                print(f"⚠️  课程 '{course_title}' 已经注册过了")
                continue
            
            # 创建注册记录
            progress = 20.0 + (i * 15)  # 模拟不同的学习进度
            completed_lessons = i + 1
            total_study_time = (i + 1) * 60  # 分钟
            enrolled_at = datetime.now() - timedelta(days=7 - i)
            last_accessed = datetime.now() - timedelta(hours=i + 1)
            
            cursor.execute("""
                INSERT INTO course_enrollments (
                    course_id, student_id, progress_percentage, completed_lessons,
                    total_study_time, is_completed, enrolled_at, last_accessed, is_active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                course_id, student_id, progress, completed_lessons,
                total_study_time, False, enrolled_at.isoformat(), 
                last_accessed.isoformat(), True
            ))
            
            enrolled_count += 1
            print(f"✅ 注册课程: {course_title}")
        
        # 提交更改
        conn.commit()
        
        print(f"\n🎉 成功创建 {enrolled_count} 个注册记录")
        
        # 验证创建的数据
        print("\n=== 验证创建的数据 ===")
        cursor.execute("""
            SELECT ce.id, c.title, ce.progress_percentage, ce.enrolled_at
            FROM course_enrollments ce
            JOIN courses c ON ce.course_id = c.id
            WHERE ce.student_id = ?
            ORDER BY ce.enrolled_at DESC
        """, (student_id,))
        
        enrollments = cursor.fetchall()
        
        for enrollment in enrollments:
            enrollment_id, course_title, progress, enrolled_at = enrollment
            print(f"- 课程: {course_title}")
            print(f"  进度: {progress}%")
            print(f"  注册时间: {enrolled_at}")
            print()
        
        print("✅ 数据创建完成！")
        
    except sqlite3.Error as e:
        print(f"❌ 数据库操作失败: {e}")
    except Exception as e:
        print(f"❌ 创建数据失败: {e}")
    finally:
        if conn:
            conn.close()


def check_database_status():
    """检查数据库状态"""
    db_path = os.path.join(os.path.dirname(__file__), "database", "data", "education_platform.db")
    
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("=== 数据库状态检查 ===")
        
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['users', 'courses', 'course_enrollments']
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            print(f"❌ 缺少必要的表: {missing_tables}")
            return False
        
        print("✅ 所有必要的表都存在")
        
        # 检查数据
        for table in required_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  - {table}: {count} 条记录")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ 数据库检查失败: {e}")
        return False


def main():
    """主函数"""
    print("🚀 开始创建课程注册测试数据...")
    
    # 检查数据库状态
    if not check_database_status():
        print("\n❌ 数据库状态检查失败，请先确保数据库正常")
        return
    
    # 创建测试数据
    create_enrollment_data()
    
    print("\n📋 建议接下来的操作:")
    print("1. 启动后端服务: python run.py")
    print("2. 访问前端页面: http://localhost:5173/student/dashboard")
    print("3. 检查'我的课程'部分是否显示真实数据")


if __name__ == "__main__":
    main()
