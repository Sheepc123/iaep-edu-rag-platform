# Python编程基础教程

## 第一章 Python简介

### 1.1 什么是Python

Python是一种高级编程语言，由Guido van Rossum于1989年发明。Python具有以下特点：

- **简单易学**：Python语法简洁明了，接近自然语言
- **跨平台**：可以在Windows、Linux、macOS等系统上运行
- **开源免费**：Python是开源软件，可以自由使用和分发
- **功能强大**：拥有丰富的标准库和第三方库
- **应用广泛**：可用于Web开发、数据分析、人工智能、自动化等领域

### 1.2 Python的应用领域

1. **Web开发**：Django、Flask等框架
2. **数据科学**：NumPy、Pandas、Matplotlib等库
3. **人工智能**：TensorFlow、PyTorch等深度学习框架
4. **自动化脚本**：系统管理、文件处理等
5. **游戏开发**：Pygame等游戏引擎

## 第二章 Python环境搭建

### 2.1 安装Python

#### Windows系统安装
1. 访问Python官网 https://www.python.org/
2. 下载最新版本的Python安装包
3. 运行安装程序，勾选"Add Python to PATH"
4. 点击"Install Now"完成安装

#### 验证安装
打开命令提示符，输入以下命令：
```bash
python --version
```

如果显示Python版本号，说明安装成功。

### 2.2 开发环境选择

推荐的Python开发环境：
- **PyCharm**：功能强大的IDE
- **VS Code**：轻量级编辑器，插件丰富
- **Jupyter Notebook**：适合数据分析和学习
- **IDLE**：Python自带的简单IDE

## 第三章 Python基础语法

### 3.1 变量和数据类型

#### 变量定义
Python中的变量不需要声明类型，直接赋值即可：
```python
name = "张三"
age = 25
height = 1.75
is_student = True
```

#### 基本数据类型
1. **整数（int）**：如 10, -5, 0
2. **浮点数（float）**：如 3.14, -2.5
3. **字符串（str）**：如 "Hello", '世界'
4. **布尔值（bool）**：True 或 False

#### 类型转换
```python
# 字符串转整数
num = int("123")

# 整数转字符串
text = str(456)

# 字符串转浮点数
price = float("19.99")
```

### 3.2 运算符

#### 算术运算符
```python
a = 10
b = 3

print(a + b)    # 加法：13
print(a - b)    # 减法：7
print(a * b)    # 乘法：30
print(a / b)    # 除法：3.333...
print(a // b)   # 整除：3
print(a % b)    # 取余：1
print(a ** b)   # 幂运算：1000
```

#### 比较运算符
```python
x = 5
y = 8

print(x == y)   # 等于：False
print(x != y)   # 不等于：True
print(x < y)    # 小于：True
print(x > y)    # 大于：False
print(x <= y)   # 小于等于：True
print(x >= y)   # 大于等于：False
```

#### 逻辑运算符
```python
a = True
b = False

print(a and b)  # 与：False
print(a or b)   # 或：True
print(not a)    # 非：False
```

### 3.3 字符串操作

#### 字符串创建
```python
# 单引号
str1 = 'Hello'

# 双引号
str2 = "World"

# 三引号（多行字符串）
str3 = """这是一个
多行字符串"""
```

#### 字符串方法
```python
text = "Python Programming"

print(text.upper())      # 转大写：PYTHON PROGRAMMING
print(text.lower())      # 转小写：python programming
print(text.title())      # 标题格式：Python Programming
print(text.replace("Python", "Java"))  # 替换：Java Programming
print(text.split())      # 分割：['Python', 'Programming']
print(len(text))         # 长度：18
```

#### 字符串格式化
```python
name = "小明"
age = 20
score = 95.5

# f-string格式化（推荐）
message = f"学生{name}，年龄{age}岁，成绩{score}分"

# format方法
message = "学生{}，年龄{}岁，成绩{:.1f}分".format(name, age, score)

# %格式化
message = "学生%s，年龄%d岁，成绩%.1f分" % (name, age, score)
```

## 第四章 控制结构

### 4.1 条件语句

#### if语句
```python
score = 85

if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 70:
    print("中等")
elif score >= 60:
    print("及格")
else:
    print("不及格")
```

#### 条件表达式（三元运算符）
```python
age = 18
status = "成年人" if age >= 18 else "未成年人"
```

### 4.2 循环语句

#### for循环
```python
# 遍历数字
for i in range(5):
    print(i)  # 输出：0, 1, 2, 3, 4

# 遍历列表
fruits = ["苹果", "香蕉", "橙子"]
for fruit in fruits:
    print(fruit)

# 遍历字符串
for char in "Python":
    print(char)
```

#### while循环
```python
count = 0
while count < 5:
    print(f"第{count + 1}次循环")
    count += 1
```

#### 循环控制
```python
for i in range(10):
    if i == 3:
        continue  # 跳过本次循环
    if i == 7:
        break     # 跳出循环
    print(i)
```

## 第五章 数据结构

### 5.1 列表（List）

#### 列表创建和操作
```python
# 创建列表
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# 访问元素
print(numbers[0])    # 第一个元素：1
print(numbers[-1])   # 最后一个元素：5

# 切片
print(numbers[1:4])  # [2, 3, 4]
print(numbers[:3])   # [1, 2, 3]
print(numbers[2:])   # [3, 4, 5]

# 修改元素
numbers[0] = 10
print(numbers)       # [10, 2, 3, 4, 5]
```

#### 列表方法
```python
fruits = ["苹果", "香蕉"]

# 添加元素
fruits.append("橙子")        # 末尾添加
fruits.insert(1, "葡萄")     # 指定位置插入

# 删除元素
fruits.remove("香蕉")        # 删除指定元素
last_fruit = fruits.pop()    # 删除并返回最后一个元素

# 其他操作
print(len(fruits))           # 列表长度
print("苹果" in fruits)      # 检查元素是否存在
fruits.sort()                # 排序
fruits.reverse()             # 反转
```

### 5.2 元组（Tuple）

```python
# 创建元组
point = (3, 4)
colors = ("红", "绿", "蓝")

# 元组是不可变的
print(point[0])      # 访问元素：3
# point[0] = 5       # 错误！元组不能修改

# 元组解包
x, y = point
print(f"坐标：({x}, {y})")
```

### 5.3 字典（Dictionary）

```python
# 创建字典
student = {
    "name": "张三",
    "age": 20,
    "major": "计算机科学"
}

# 访问和修改
print(student["name"])       # 张三
student["age"] = 21          # 修改值
student["grade"] = "大二"    # 添加新键值对

# 字典方法
print(student.keys())        # 所有键
print(student.values())      # 所有值
print(student.items())       # 所有键值对

# 安全访问
grade = student.get("grade", "未知")  # 如果键不存在返回默认值
```

### 5.4 集合（Set）

```python
# 创建集合
numbers = {1, 2, 3, 4, 5}
fruits = set(["苹果", "香蕉", "苹果"])  # 自动去重

# 集合操作
numbers.add(6)           # 添加元素
numbers.remove(1)        # 删除元素

# 集合运算
set1 = {1, 2, 3}
set2 = {3, 4, 5}

print(set1 | set2)       # 并集：{1, 2, 3, 4, 5}
print(set1 & set2)       # 交集：{3}
print(set1 - set2)       # 差集：{1, 2}
```

## 第六章 函数

### 6.1 函数定义和调用

```python
# 定义函数
def greet(name):
    """问候函数"""
    return f"你好，{name}！"

# 调用函数
message = greet("小明")
print(message)  # 你好，小明！
```

### 6.2 参数类型

```python
# 默认参数
def power(base, exponent=2):
    return base ** exponent

print(power(3))      # 9 (3的2次方)
print(power(3, 3))   # 27 (3的3次方)

# 可变参数
def sum_all(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total

print(sum_all(1, 2, 3, 4, 5))  # 15

# 关键字参数
def create_profile(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

create_profile(name="张三", age=25, city="北京")
```

### 6.3 Lambda函数

```python
# Lambda函数（匿名函数）
square = lambda x: x ** 2
print(square(5))  # 25

# 与内置函数结合使用
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)  # [2, 4]
```

## 第七章 面向对象编程

### 7.1 类和对象

```python
class Student:
    """学生类"""
    
    def __init__(self, name, age, major):
        """构造方法"""
        self.name = name
        self.age = age
        self.major = major
        self.courses = []
    
    def add_course(self, course):
        """添加课程"""
        self.courses.append(course)
    
    def get_info(self):
        """获取学生信息"""
        return f"姓名：{self.name}，年龄：{self.age}，专业：{self.major}"

# 创建对象
student1 = Student("张三", 20, "计算机科学")
student1.add_course("Python编程")
print(student1.get_info())
```

### 7.2 继承

```python
class Person:
    """人类基类"""
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"我是{self.name}，今年{self.age}岁"

class Student(Person):
    """学生类，继承自Person"""
    
    def __init__(self, name, age, student_id):
        super().__init__(name, age)  # 调用父类构造方法
        self.student_id = student_id
    
    def introduce(self):
        return f"我是学生{self.name}，学号{self.student_id}"

# 使用继承
student = Student("李四", 19, "2023001")
print(student.introduce())
```

## 第八章 异常处理

### 8.1 try-except语句

```python
try:
    num = int(input("请输入一个数字："))
    result = 10 / num
    print(f"结果：{result}")
except ValueError:
    print("输入的不是有效数字！")
except ZeroDivisionError:
    print("不能除以零！")
except Exception as e:
    print(f"发生了未知错误：{e}")
else:
    print("计算成功完成")
finally:
    print("程序执行结束")
```

### 8.2 自定义异常

```python
class CustomError(Exception):
    """自定义异常类"""
    pass

def check_age(age):
    if age < 0:
        raise CustomError("年龄不能为负数")
    if age > 150:
        raise CustomError("年龄不能超过150岁")
    return True

try:
    check_age(-5)
except CustomError as e:
    print(f"错误：{e}")
```

## 第九章 文件操作

### 9.1 文件读写

```python
# 写入文件
with open("test.txt", "w", encoding="utf-8") as file:
    file.write("Hello, Python!\n")
    file.write("这是第二行\n")

# 读取文件
with open("test.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content)

# 逐行读取
with open("test.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
```

### 9.2 JSON文件处理

```python
import json

# 写入JSON文件
data = {
    "name": "张三",
    "age": 25,
    "courses": ["Python", "Java", "C++"]
}

with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

# 读取JSON文件
with open("data.json", "r", encoding="utf-8") as file:
    loaded_data = json.load(file)
    print(loaded_data)
```

## 第十章 模块和包

### 10.1 导入模块

```python
# 导入整个模块
import math
print(math.pi)
print(math.sqrt(16))

# 导入特定函数
from math import pi, sqrt
print(pi)
print(sqrt(25))

# 使用别名
import numpy as np
import pandas as pd
```

### 10.2 创建自定义模块

```python
# 文件：mymodule.py
def add(a, b):
    """加法函数"""
    return a + b

def multiply(a, b):
    """乘法函数"""
    return a * b

PI = 3.14159

# 在其他文件中使用
from mymodule import add, multiply, PI
print(add(3, 5))
print(multiply(4, 6))
print(PI)
```

## 总结

Python是一门功能强大且易于学习的编程语言。通过本教程，您已经学习了：

1. Python的基本语法和数据类型
2. 控制结构（条件语句和循环）
3. 数据结构（列表、元组、字典、集合）
4. 函数的定义和使用
5. 面向对象编程基础
6. 异常处理机制
7. 文件操作
8. 模块和包的使用

继续练习和探索，您将能够使用Python解决各种实际问题！
