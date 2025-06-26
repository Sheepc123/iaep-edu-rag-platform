"""
AI课程生成服务
根据文档内容生成结构化的课程信息
"""
import json
import re
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from ..core.config import settings

logger = logging.getLogger(__name__)


class AICourseGenerator:
    """AI课程生成器"""
    
    def __init__(self):
        self.max_lessons = 20  # 最大课时数
        self.min_lesson_duration = 5  # 最小课时时长(分钟)
        self.max_lesson_duration = 60  # 最大课时时长(分钟)
    
    def generate_course_from_text(self, text_content: str, filename: str = "") -> Dict[str, Any]:
        """根据文本内容生成课程结构"""
        try:
            # 分析文档内容
            content_analysis = self._analyze_content(text_content)
            
            # 生成课程基本信息
            course_info = self._generate_course_info(content_analysis, filename)
            
            # 生成课程大纲和课时
            lessons = self._generate_lessons(content_analysis)
            
            # 计算总时长
            total_duration = sum(lesson.get('duration', 30) for lesson in lessons)
            
            return {
                "title": course_info["title"],
                "description": course_info["description"],
                "category": course_info["category"],
                "difficulty": course_info["difficulty"],
                "duration": total_duration,
                "cover_image": "",
                "is_published": False,
                "lessons": lessons,
                "generated_at": datetime.utcnow().isoformat(),
                "source_info": {
                    "filename": filename,
                    "word_count": len(text_content.split()),
                    "estimated_reading_time": max(1, len(text_content.split()) // 200)
                }
            }
            
        except Exception as e:
            logger.error(f"AI课程生成失败: {str(e)}")
            # 返回默认课程结构
            return self._generate_default_course(filename)
    
    def _analyze_content(self, text_content: str) -> Dict[str, Any]:
        """分析文档内容"""
        lines = text_content.split('\n')
        paragraphs = [line.strip() for line in lines if line.strip()]
        
        # 提取可能的标题（通常是较短的行或包含特定关键词）
        potential_titles = []
        potential_sections = []
        
        for line in paragraphs[:20]:  # 只分析前20段
            line = line.strip()
            if len(line) < 100 and len(line) > 5:  # 可能的标题
                potential_titles.append(line)
            
            # 查找章节标题（包含数字或特定关键词）
            if re.match(r'^(第?\d+[章节课]|Chapter\s+\d+|\d+\.|一、|二、|三、)', line, re.IGNORECASE):
                potential_sections.append(line)
        
        # 分析主题和关键词
        keywords = self._extract_keywords(text_content)
        
        return {
            "total_paragraphs": len(paragraphs),
            "word_count": len(text_content.split()),
            "potential_titles": potential_titles,
            "potential_sections": potential_sections,
            "keywords": keywords,
            "estimated_complexity": self._estimate_complexity(text_content)
        }
    
    def _extract_keywords(self, text_content: str) -> List[str]:
        """提取关键词"""
        # 简单的关键词提取（实际项目中可以使用更复杂的NLP技术）
        common_course_keywords = [
            "编程", "程序设计", "算法", "数据结构", "数据库", "网络", "系统",
            "管理", "营销", "财务", "会计", "经济", "金融",
            "设计", "美术", "音乐", "文学", "历史", "哲学",
            "数学", "物理", "化学", "生物", "医学",
            "英语", "语言", "翻译", "写作"
        ]
        
        found_keywords = []
        text_lower = text_content.lower()
        
        for keyword in common_course_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords[:10]  # 返回前10个关键词
    
    def _estimate_complexity(self, text_content: str) -> str:
        """估算内容复杂度"""
        word_count = len(text_content.split())
        
        # 检查技术术语密度
        technical_terms = ["API", "算法", "数据结构", "框架", "架构", "设计模式", "优化"]
        technical_count = sum(1 for term in technical_terms if term in text_content)
        
        if word_count > 5000 or technical_count > 3:
            return "hard"
        elif word_count > 2000 or technical_count > 1:
            return "medium"
        else:
            return "easy"
    
    def _generate_course_info(self, analysis: Dict[str, Any], filename: str) -> Dict[str, Any]:
        """生成课程基本信息"""
        # 生成课程标题
        if analysis["potential_titles"]:
            title = analysis["potential_titles"][0]
        elif filename:
            title = filename.replace('.pdf', '').replace('.docx', '').replace('.doc', '')
        else:
            title = "AI生成课程"
        
        # 生成课程描述
        description = self._generate_description(analysis)
        
        # 确定课程分类
        category = self._determine_category(analysis["keywords"])
        
        return {
            "title": title,
            "description": description,
            "category": category,
            "difficulty": analysis["estimated_complexity"]
        }
    
    def _generate_description(self, analysis: Dict[str, Any]) -> str:
        """生成课程描述"""
        base_description = "本课程基于AI智能分析生成，"
        
        if analysis["keywords"]:
            keywords_str = "、".join(analysis["keywords"][:5])
            base_description += f"主要涵盖{keywords_str}等内容。"
        
        base_description += f"课程包含{len(analysis['potential_sections'])}个主要章节，"
        base_description += f"预计学习时长{analysis['word_count'] // 200}分钟。"
        
        if analysis["estimated_complexity"] == "hard":
            base_description += "适合有一定基础的学习者深入学习。"
        elif analysis["estimated_complexity"] == "medium":
            base_description += "适合有基础知识的学习者进阶学习。"
        else:
            base_description += "适合初学者入门学习。"
        
        return base_description
    
    def _determine_category(self, keywords: List[str]) -> str:
        """确定课程分类"""
        category_mapping = {
            "programming": ["编程", "程序设计", "算法", "数据结构", "开发"],
            "business": ["管理", "营销", "财务", "会计", "经济", "金融"],
            "design": ["设计", "美术", "UI", "UX", "平面设计"],
            "language": ["英语", "语言", "翻译", "写作"],
            "science": ["数学", "物理", "化学", "生物", "医学"],
            "humanities": ["文学", "历史", "哲学", "社会学"]
        }
        
        for category, category_keywords in category_mapping.items():
            if any(keyword in keywords for keyword in category_keywords):
                return category
        
        return "other"
    
    def _generate_lessons(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成课时列表"""
        lessons = []
        
        # 如果有明确的章节结构，使用章节作为课时
        if analysis["potential_sections"]:
            for i, section in enumerate(analysis["potential_sections"][:self.max_lessons]):
                lesson = {
                    "title": section,
                    "description": f"学习{section}的相关内容和要点",
                    "content": f"本课时将详细讲解{section}的核心概念和实践应用。",
                    "duration": min(max(analysis["word_count"] // len(analysis["potential_sections"]) // 10, 
                                       self.min_lesson_duration), self.max_lesson_duration),
                    "lesson_type": "text",
                    "lesson_order": i + 1,
                    "video_url": "",
                    "materials": [],
                    "is_published": False,
                    "is_free": i == 0  # 第一课时免费
                }
                lessons.append(lesson)
        else:
            # 如果没有明确章节，生成通用课时结构
            default_lessons = [
                "课程介绍与概述",
                "基础概念讲解", 
                "核心内容学习",
                "实践案例分析",
                "总结与拓展"
            ]
            
            for i, lesson_title in enumerate(default_lessons):
                lesson = {
                    "title": lesson_title,
                    "description": f"本课时主要学习{lesson_title}相关内容",
                    "content": f"通过本课时的学习，您将掌握{lesson_title}的核心要点。",
                    "duration": 30,  # 默认30分钟
                    "lesson_type": "text",
                    "lesson_order": i + 1,
                    "video_url": "",
                    "materials": [],
                    "is_published": False,
                    "is_free": i == 0
                }
                lessons.append(lesson)
        
        return lessons
    
    def _generate_default_course(self, filename: str = "") -> Dict[str, Any]:
        """生成默认课程结构（当AI生成失败时使用）"""
        title = filename.replace('.pdf', '').replace('.docx', '').replace('.doc', '') if filename else "新课程"
        
        return {
            "title": title,
            "description": "基于上传文档生成的课程，请根据需要调整课程内容。",
            "category": "other",
            "difficulty": "medium",
            "duration": 120,
            "cover_image": "",
            "is_published": False,
            "lessons": [
                {
                    "title": "课程介绍",
                    "description": "课程概述和学习目标",
                    "content": "欢迎学习本课程！",
                    "duration": 30,
                    "lesson_type": "text",
                    "lesson_order": 1,
                    "video_url": "",
                    "materials": [],
                    "is_published": False,
                    "is_free": True
                }
            ],
            "generated_at": datetime.utcnow().isoformat(),
            "source_info": {
                "filename": filename,
                "generation_method": "default"
            }
        }
