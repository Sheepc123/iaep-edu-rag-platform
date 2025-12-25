"""
知识库增强的AI生成服务
整合DeepSeek向量搜索和AI生成功能，为课程和习题生成提供统一的知识库支持
"""
import json
import asyncio
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from loguru import logger

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.services.vector_service_deepseek import get_deepseek_vector_service
from app.services.teacher_knowledge_service import TeacherKnowledgeService
from app.services.ai_service import AIService
from app.services.course_service import CourseService
from app.services.exercise_service import ExerciseService
from app.models.knowledge_base import TeacherKnowledgeDoc
from app.schemas.course import CourseCreate
from app.schemas.exercise import ExerciseCreate, QuestionCreate, QuestionType, DifficultyLevel
from app.core.config import settings


class AIKnowledgeGenerator:
    """知识库增强的AI生成服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.vector_service = get_deepseek_vector_service()
        self.knowledge_service = TeacherKnowledgeService(db)
        self.ai_service = AIService(db)
        self.course_service = CourseService(db)
        self.exercise_service = ExerciseService(db)
    
    async def generate_course_from_knowledge(
        self,
        teacher_id: int,
        topic: str,
        knowledge_doc_ids: Optional[List[int]] = None,
        course_level: str = "medium",
        lesson_count: int = 8,
        auto_save: bool = False
    ) -> Dict[str, Any]:
        """
        基于知识库文档生成课程
        
        Args:
            teacher_id: 教师ID
            topic: 课程主题
            knowledge_doc_ids: 指定的知识库文档ID列表，如果为空则搜索相关文档
            course_level: 课程难度级别
            lesson_count: 课时数量
            auto_save: 是否自动保存课程
            
        Returns:
            生成的课程数据
        """
        try:
            logger.info(f"开始为教师 {teacher_id} 基于知识库生成课程: {topic}")
            
            # 1. 获取相关知识库内容
            knowledge_content = await self._get_relevant_knowledge_content(
                teacher_id, topic, knowledge_doc_ids
            )
            
            if not knowledge_content:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="未找到相关的知识库内容，请先上传相关文档或检查搜索主题"
                )
            
            # 2. 构建课程生成提示词
            course_prompt = self._build_course_generation_prompt(
                topic, knowledge_content, course_level, lesson_count
            )
            
            # 3. 调用AI生成课程结构
            generated_course = await self._call_ai_for_course_generation(course_prompt)
            
            # 4. 处理生成结果
            course_data = self._process_generated_course(
                generated_course, topic, knowledge_content
            )
            
            # 5. 如果需要自动保存，保存到数据库
            saved_course = None
            if auto_save:
                saved_course = await self._save_generated_course(course_data, teacher_id)
            
            return {
                "success": True,
                "message": "基于知识库的课程生成成功",
                "course_data": course_data,
                "saved_course": saved_course,
                "knowledge_sources": [
                    {
                        "doc_id": doc["doc_id"],
                        "title": doc["title"],
                        "relevance_score": doc.get("similarity", 0.0)
                    }
                    for doc in knowledge_content
                ],
                "generation_info": {
                    "topic": topic,
                    "difficulty": course_level,
                    "lesson_count": lesson_count,
                    "knowledge_docs_used": len(knowledge_content),
                    "generated_at": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"基于知识库生成课程失败: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"课程生成失败: {str(e)}"
            )
    
    async def generate_exercises_from_knowledge(
        self,
        teacher_id: int,
        topic: str,
        knowledge_doc_ids: Optional[List[int]] = None,
        exercise_types: List[str] = None,
        difficulty: str = "medium",
        question_count: int = 10,
        auto_save: bool = False,
        course_id: Optional[int] = None,
        exercise_category: str = "自主练习"
    ) -> Dict[str, Any]:
        """
        基于知识库文档生成习题
        
        Args:
            teacher_id: 教师ID
            topic: 习题主题
            knowledge_doc_ids: 指定的知识库文档ID列表
            exercise_types: 题目类型列表
            difficulty: 难度级别
            question_count: 题目数量
            auto_save: 是否自动保存习题
            course_id: 关联的课程ID
            
        Returns:
            生成的习题数据
        """
        try:
            logger.info(f"开始为教师 {teacher_id} 基于知识库生成习题: {topic}")
            
            # 设置默认题目类型
            if not exercise_types:
                exercise_types = ["multiple_choice", "fill_blank", "essay"]
            
            # 1. 获取相关知识库内容
            knowledge_content = await self._get_relevant_knowledge_content(
                teacher_id, topic, knowledge_doc_ids
            )
            
            if not knowledge_content:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="未找到相关的知识库内容，请先上传相关文档或检查搜索主题"
                )
            
            # 2. 构建习题生成提示词
            exercise_prompt = self._build_exercise_generation_prompt(
                topic, knowledge_content, exercise_types, difficulty, question_count
            )
            
            # 3. 调用AI生成习题 - 使用现有的AI服务
            generated_exercises = await self._call_ai_service_for_exercises(
                topic, exercise_types, difficulty, question_count, knowledge_content
            )
            
            # 4. 处理生成结果
            exercise_data = self._process_generated_exercises(
                generated_exercises, topic, knowledge_content, course_id, exercise_category
            )
            
            # 5. 如果需要自动保存，保存到数据库
            saved_exercise = None
            if auto_save:
                saved_exercise = await self._save_generated_exercises(
                    exercise_data, teacher_id, course_id
                )
            
            return {
                "success": True,
                "message": "基于知识库的习题生成成功",
                "exercise_data": exercise_data,
                "saved_exercise": saved_exercise,
                "knowledge_sources": [
                    {
                        "doc_id": doc["doc_id"],
                        "title": doc["title"],
                        "relevance_score": doc.get("similarity", 0.0)
                    }
                    for doc in knowledge_content
                ],
                "generation_info": {
                    "topic": topic,
                    "difficulty": difficulty,
                    "question_count": question_count,
                    "exercise_types": exercise_types,
                    "knowledge_docs_used": len(knowledge_content),
                    "generated_at": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"基于知识库生成习题失败: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"习题生成失败: {str(e)}"
            )
    
    async def _get_relevant_knowledge_content(
        self,
        teacher_id: int,
        topic: str,
        knowledge_doc_ids: Optional[List[int]] = None
    ) -> List[Dict[str, Any]]:
        """获取相关的知识库内容"""
        try:
            knowledge_content = []
            
            if knowledge_doc_ids:
                # 如果指定了文档ID，直接获取这些文档
                for doc_id in knowledge_doc_ids:
                    doc = self.db.query(TeacherKnowledgeDoc).filter(
                        TeacherKnowledgeDoc.id == doc_id,
                        TeacherKnowledgeDoc.teacher_id == teacher_id,
                        TeacherKnowledgeDoc.status == "active"
                    ).first()
                    
                    if doc and doc.text_content:
                        knowledge_content.append({
                            "doc_id": doc.id,
                            "title": doc.title,
                            "content": doc.text_content[:5000],  # 限制长度
                            "category": doc.category,
                            "similarity": 1.0  # 指定文档认为完全相关
                        })
            else:
                # 使用语义搜索找到相关文档
                if self.vector_service.is_available():
                    search_results = self.vector_service.search_similar(
                        query=topic,
                        top_k=5,
                        filter_metadata={"teacher_id": teacher_id}
                    )
                    
                    for result in search_results:
                        doc_id = result.get("metadata", {}).get("doc_id")
                        if doc_id:
                            doc = self.db.query(TeacherKnowledgeDoc).filter(
                                TeacherKnowledgeDoc.id == doc_id,
                                TeacherKnowledgeDoc.teacher_id == teacher_id
                            ).first()
                            
                            if doc and doc.text_content:
                                knowledge_content.append({
                                    "doc_id": doc.id,
                                    "title": doc.title,
                                    "content": result.get("document", doc.text_content[:5000]),
                                    "category": doc.category,
                                    "similarity": 1.0 - result.get("distance", 0.5)
                                })
                
                # 如果向量搜索没有结果，回退到关键词搜索
                if not knowledge_content:
                    search_results = self.knowledge_service.search_documents(
                        teacher_id=teacher_id,
                        query=topic,
                        limit=5
                    )

                    for result in search_results:
                        # 处理不同类型的搜索结果
                        if hasattr(result, 'text_content'):
                            # 直接的文档对象
                            content = result.text_content[:5000] if result.text_content else ""
                            doc_id = result.id
                            title = result.title
                            category = result.category
                        else:
                            # KnowledgeSearchResult 对象
                            content = getattr(result, 'content', '')[:5000] if getattr(result, 'content', '') else ""
                            doc_id = getattr(result, 'id', 0)
                            title = getattr(result, 'title', '未知文档')
                            category = getattr(result, 'category', '其他')

                        knowledge_content.append({
                            "doc_id": doc_id,
                            "title": title,
                            "content": content,
                            "category": category,
                            "similarity": 0.8  # 关键词搜索的默认相关度
                        })
            
            logger.info(f"为主题 '{topic}' 找到 {len(knowledge_content)} 个相关文档")
            return knowledge_content

        except Exception as e:
            logger.error(f"获取知识库内容失败: {str(e)}")
            return []

    def _build_course_generation_prompt(
        self,
        topic: str,
        knowledge_content: List[Dict[str, Any]],
        course_level: str,
        lesson_count: int
    ) -> str:
        """构建课程生成提示词"""

        # 整理知识库内容
        knowledge_text = ""
        for i, doc in enumerate(knowledge_content[:3], 1):  # 最多使用前3个最相关的文档
            knowledge_text += f"\n=== 参考文档 {i}: {doc['title']} ===\n"
            knowledge_text += doc['content'][:2000]  # 每个文档最多2000字符
            knowledge_text += "\n"

        prompt = f"""
你是一位专业的教育课程设计专家。请基于提供的知识库内容，为主题"{topic}"设计一个完整的课程。

## 知识库参考内容：
{knowledge_text}

## 课程设计要求：
- 课程主题：{topic}
- 难度级别：{course_level}
- 课时数量：{lesson_count}个课时
- 每个课时建议时长：30-60分钟

## 请按以下JSON格式输出课程设计（注意：必须是有效的JSON格式，不要包含注释）：

{{
    "title": "课程标题",
    "description": "课程详细描述，包括学习目标、适用对象等",
    "category": "课程分类",
    "difficulty": "{course_level}",
    "duration": 480,
    "lessons": [
        {{
            "title": "课时标题",
            "description": "课时描述",
            "content": "课时详细内容",
            "duration": 60,
            "lesson_type": "text",
            "lesson_order": 1,
            "is_free": true
        }}
    ]
}}

## 设计原则：
1. 课程内容必须基于提供的知识库内容
2. 课程结构要循序渐进，符合学习规律
3. 每个课时都要有明确的学习目标
4. 第一个课时设为免费，其他课时收费
5. 课程描述要详细，包含学习收获
6. 课时内容要具体实用，不要空泛

请确保输出的是有效的JSON格式。
"""
        return prompt

    def _build_exercise_generation_prompt(
        self,
        topic: str,
        knowledge_content: List[Dict[str, Any]],
        exercise_types: List[str],
        difficulty: str,
        question_count: int
    ) -> str:
        """构建习题生成提示词"""

        # 整理知识库内容
        knowledge_text = ""
        for i, doc in enumerate(knowledge_content[:3], 1):
            knowledge_text += f"\n=== 参考文档 {i}: {doc['title']} ===\n"
            knowledge_text += doc['content'][:2000]
            knowledge_text += "\n"

        # 题型说明
        type_descriptions = {
            "multiple_choice": "选择题（4个选项，A/B/C/D）",
            "fill_blank": "填空题",
            "essay": "简答题",
            "true_false": "判断题"
        }

        types_text = "、".join([type_descriptions.get(t, t) for t in exercise_types])

        prompt = f"""
你是一位专业的教育测评专家。请基于提供的知识库内容，为主题"{topic}"设计习题。

## 知识库参考内容：
{knowledge_text}

## 习题设计要求：
- 习题主题：{topic}
- 题目类型：{types_text}
- 难度级别：{difficulty}
- 题目数量：{question_count}道题
- 题目分值：每题10分

## 请按以下JSON格式输出习题设计（注意：必须是有效的JSON格式，不要包含注释）：

{{
    "exercise_title": "习题集标题",
    "exercise_description": "习题集描述",
    "questions": [
        {{
            "title": "题目标题",
            "content": "题目内容",
            "question_type": "multiple_choice",
            "options": {{"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"}},
            "correct_answer": "A",
            "explanation": "答案解析",
            "difficulty": "{difficulty}",
            "points": 10,
            "subject": "科目",
            "tags": ["标签1", "标签2"]
        }}
    ]
}}

## 设计原则：
1. 题目内容必须基于提供的知识库内容
2. 选择题的选项要合理，干扰项要有一定迷惑性
3. 填空题的空格要设置在关键知识点上
4. 简答题要考查理解和应用能力
5. 每道题都要有详细的答案解析
6. 题目难度要符合指定级别
7. 题目要覆盖知识库内容的不同方面

注意：
- 选择题的correct_answer必须是A、B、C、D中的一个
- options字段只有选择题需要，其他题型设为null
- 确保输出的是有效的JSON格式

请确保输出的是有效的JSON格式。
"""
        return prompt

    async def _call_ai_for_course_generation(self, prompt: str) -> Dict[str, Any]:
        """调用AI生成课程"""
        try:
            if settings.DEEPSEEK_API_KEY and settings.DEEPSEEK_API_KEY != "your-deepseek-api-key-here":
                # 使用DeepSeek API
                result = await self.ai_service._call_deepseek_api(
                    prompt, conversation_id=0, user_role="teacher"
                )

                # 尝试解析JSON
                if isinstance(result, dict) and "content" in result:
                    content = result["content"]
                else:
                    content = str(result)

                # 提取JSON内容
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_content = content[json_start:json_end]
                    try:
                        # 尝试清理JSON内容
                        json_content = self._clean_json_content(json_content)
                        return json.loads(json_content)
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON解析失败: {e}")
                        logger.error(f"原始内容: {json_content[:500]}...")
                        logger.warning("使用模拟数据替代")
                        return self._generate_mock_course()
                else:
                    logger.warning("AI响应中未找到有效的JSON格式，使用模拟数据")
                    return self._generate_mock_course()
            else:
                # 返回模拟数据
                return self._generate_mock_course()

        except Exception as e:
            logger.error(f"AI课程生成失败: {str(e)}")
            return self._generate_mock_course()

    async def _call_ai_for_exercise_generation(self, prompt: str) -> Dict[str, Any]:
        """调用AI生成习题"""
        try:
            if settings.DEEPSEEK_API_KEY and settings.DEEPSEEK_API_KEY != "your-deepseek-api-key-here":
                # 使用DeepSeek API
                result = await self.ai_service._call_deepseek_api(
                    prompt, conversation_id=0, user_role="teacher"
                )

                # 尝试解析JSON
                if isinstance(result, dict) and "content" in result:
                    content = result["content"]
                else:
                    content = str(result)

                # 提取JSON内容
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_content = content[json_start:json_end]
                    try:
                        # 尝试清理JSON内容
                        json_content = self._clean_json_content(json_content)
                        return json.loads(json_content)
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON解析失败: {e}")
                        logger.error(f"原始内容: {json_content[:500]}...")
                        logger.warning("使用模拟数据替代")
                        return self._generate_mock_exercises()
                else:
                    logger.warning("AI响应中未找到有效的JSON格式，使用模拟数据")
                    return self._generate_mock_exercises()
            else:
                # 返回模拟数据
                return self._generate_mock_exercises()

        except Exception as e:
            logger.error(f"AI习题生成失败: {str(e)}")
            return self._generate_mock_exercises()

    async def _call_ai_service_for_exercises(
        self,
        topic: str,
        exercise_types: List[str],
        difficulty: str,
        question_count: int,
        knowledge_content: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """调用现有的AI服务生成习题"""
        try:
            # 构建知识库上下文
            context_text = ""
            for doc in knowledge_content[:3]:  # 最多使用前3个文档
                context_text += f"参考文档《{doc['title']}》:\n{doc['content'][:1000]}\n\n"

            # 构建额外要求
            additional_requirements = f"""
请基于以下知识库内容生成题目：

{context_text}

要求：
1. 题目内容必须基于上述知识库内容
2. 确保题目的准确性和相关性
3. 选择题的选项要合理，干扰项要有一定迷惑性
4. 每道题都要有详细的答案解析
"""

            # 调用现有的AI服务
            result = await self.ai_service.generate_questions(
                user_id=0,  # 系统生成
                subject="综合",
                topic=topic,
                difficulty=difficulty,
                question_count=question_count,
                question_types=exercise_types,
                additional_requirements=additional_requirements
            )

            # 转换格式以匹配期望的结构
            return {
                "exercise_title": f"{topic}习题集",
                "exercise_description": f"基于知识库生成的{topic}相关习题",
                "questions": result.get("questions", [])
            }

        except Exception as e:
            logger.error(f"AI服务生成习题失败: {str(e)}")
            logger.warning("回退到模拟数据生成")
            # 生成基于知识库内容的模拟习题
            return self._generate_knowledge_based_mock_exercises(topic, exercise_types, question_count)

    def _clean_json_content(self, json_content: str) -> str:
        """清理JSON内容，移除可能导致解析错误的字符"""
        try:
            # 移除可能的注释
            lines = json_content.split('\n')
            cleaned_lines = []
            for line in lines:
                # 移除行内注释（但保留字符串内的//）
                if '//' in line and not line.strip().startswith('"'):
                    comment_pos = line.find('//')
                    # 检查//是否在字符串内
                    quote_count = line[:comment_pos].count('"')
                    if quote_count % 2 == 0:  # //不在字符串内
                        line = line[:comment_pos]
                cleaned_lines.append(line)

            cleaned_content = '\n'.join(cleaned_lines)

            # 移除多余的逗号（在}或]前的逗号）
            import re
            cleaned_content = re.sub(r',\s*([}\]])', r'\1', cleaned_content)

            return cleaned_content
        except Exception as e:
            logger.warning(f"JSON清理失败: {e}")
            return json_content

    def _process_generated_course(
        self,
        generated_course: Dict[str, Any],
        topic: str,
        knowledge_content: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """处理生成的课程数据"""
        try:
            # 确保必要字段存在
            course_data = {
                "title": generated_course.get("title", f"{topic}课程"),
                "description": generated_course.get("description", f"基于知识库生成的{topic}相关课程"),
                "category": generated_course.get("category", "综合"),
                "difficulty": generated_course.get("difficulty", "medium"),
                "duration": generated_course.get("duration", 480),  # 默认8小时
                "lessons": []
            }

            # 处理课时数据
            lessons = generated_course.get("lessons", [])
            for i, lesson in enumerate(lessons):
                lesson_data = {
                    "title": lesson.get("title", f"第{i+1}课时"),
                    "description": lesson.get("description", ""),
                    "content": lesson.get("content", ""),
                    "duration": lesson.get("duration", 60),
                    "lesson_type": lesson.get("lesson_type", "text"),
                    "lesson_order": lesson.get("lesson_order", i + 1),
                    "is_free": lesson.get("is_free", i == 0),  # 第一课时免费
                    "is_published": False
                }
                course_data["lessons"].append(lesson_data)

            return course_data

        except Exception as e:
            logger.error(f"处理课程数据失败: {str(e)}")
            return self._generate_default_course(topic)

    def _process_generated_exercises(
        self,
        generated_exercises: Dict[str, Any],
        topic: str,
        knowledge_content: List[Dict[str, Any]],
        course_id: Optional[int] = None,
        exercise_category: str = "自主练习"
    ) -> Dict[str, Any]:
        """处理生成的习题数据"""
        try:
            # 确保必要字段存在
            exercise_data = {
                "title": generated_exercises.get("exercise_title", f"{topic}习题集"),
                "description": generated_exercises.get("exercise_description", f"基于知识库生成的{topic}相关习题"),
                "category": exercise_category,  # 使用传入的分类
                "subject": topic,
                "difficulty": "medium",
                "time_limit": 60,  # 默认60分钟
                "course_id": course_id,
                "is_published": False,
                "questions": []
            }

            # 处理题目数据
            questions = generated_exercises.get("questions", [])
            for i, question in enumerate(questions):
                # 处理AI服务返回的题目格式
                question_text = question.get("question_text", question.get("content", ""))
                question_type = question.get("question_type", "multiple_choice")

                # 处理选择题选项 - 保持对象格式 {A: "选项A", B: "选项B"}
                options = None
                if question_type == "multiple_choice":
                    raw_options = question.get("options")
                    if isinstance(raw_options, dict):
                        # 确保选项格式正确
                        formatted_options = {}
                        for key, value in raw_options.items():
                            if key.upper() in ['A', 'B', 'C', 'D']:
                                formatted_options[key.upper()] = str(value)
                        options = formatted_options if len(formatted_options) >= 2 else None
                    elif isinstance(raw_options, list) and len(raw_options) >= 2:
                        # 将数组格式转换为对象格式
                        options = {}
                        for i, opt in enumerate(raw_options[:4]):
                            options[chr(65 + i)] = str(opt)  # A, B, C, D

                # 处理正确答案格式
                correct_answer = str(question.get("correct_answer", ""))
                if question_type == "multiple_choice" and options:
                    # 如果正确答案是选项内容，转换为对应的字母
                    if correct_answer.upper() not in ['A', 'B', 'C', 'D']:
                        # 在选项中查找匹配的内容
                        for key, value in options.items():
                            if value == correct_answer:
                                correct_answer = key
                                break
                        else:
                            # 如果没找到匹配的，默认设为A
                            correct_answer = "A"
                    else:
                        # 确保是大写字母
                        correct_answer = correct_answer.upper()

                question_data = {
                    "title": question.get("title", f"题目{i+1}"),
                    "content": question_text,
                    "question_type": question_type,
                    "options": options,
                    "correct_answer": correct_answer,
                    "explanation": question.get("explanation", ""),
                    "difficulty": question.get("difficulty", "medium"),
                    "points": question.get("points", 10),
                    "subject": question.get("subject", topic),
                    "tags": question.get("tags", [])
                }
                exercise_data["questions"].append(question_data)

            return exercise_data

        except Exception as e:
            logger.error(f"处理习题数据失败: {str(e)}")
            return self._generate_default_exercises(topic)

    async def _save_generated_course(
        self,
        course_data: Dict[str, Any],
        teacher_id: int
    ) -> Optional[Dict[str, Any]]:
        """保存生成的课程到数据库"""
        try:
            # 创建课程
            course_create = CourseCreate(
                title=course_data["title"],
                description=course_data["description"],
                category=course_data["category"],
                difficulty=course_data["difficulty"],
                duration=course_data["duration"],
                cover_image="",
                is_published=False
            )

            course = self.course_service.create_course(course_create, teacher_id)

            # 创建课时
            from app.schemas.course import LessonCreate, LessonType

            saved_lessons = []
            for lesson_data in course_data["lessons"]:
                # 转换lesson_type字符串为枚举
                lesson_type_str = lesson_data.get("lesson_type", "text")
                if lesson_type_str == "video":
                    lesson_type = LessonType.VIDEO
                elif lesson_type_str == "interactive":
                    lesson_type = LessonType.INTERACTIVE
                elif lesson_type_str == "quiz":
                    lesson_type = LessonType.QUIZ
                else:
                    lesson_type = LessonType.TEXT

                lesson_create = LessonCreate(
                    title=lesson_data["title"],
                    description=lesson_data["description"],
                    content=lesson_data["content"],
                    lesson_order=lesson_data["lesson_order"],
                    duration=lesson_data["duration"],
                    lesson_type=lesson_type,
                    is_published=lesson_data["is_published"],
                    is_free=lesson_data["is_free"]
                )

                lesson = self.course_service.create_lesson(course.id, lesson_create, teacher_id)
                saved_lessons.append({
                    "id": lesson.id,
                    "title": lesson.title,
                    "order": lesson.lesson_order
                })

            return {
                "course_id": course.id,
                "course_title": course.title,
                "lessons_count": len(saved_lessons),
                "lessons": saved_lessons
            }

        except Exception as e:
            logger.error(f"保存课程失败: {str(e)}")
            return None

    async def _save_generated_exercises(
        self,
        exercise_data: Dict[str, Any],
        teacher_id: int,
        course_id: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """保存生成的习题到数据库"""
        try:
            # 创建习题集
            exercise_create = ExerciseCreate(
                title=exercise_data["title"],
                description=exercise_data["description"],
                category=exercise_data["category"],
                subject=exercise_data["subject"],
                difficulty=DifficultyLevel(exercise_data["difficulty"]),
                time_limit=exercise_data["time_limit"],
                course_id=course_id,
                is_published=exercise_data["is_published"]
            )

            exercise = self.exercise_service.create_exercise(exercise_create, teacher_id)

            # 创建题目
            saved_questions = []
            for question_data in exercise_data["questions"]:
                question_create = QuestionCreate(
                    title=question_data["title"],
                    content=question_data["content"],
                    question_type=QuestionType(question_data["question_type"]),
                    options=question_data["options"],
                    correct_answer=question_data["correct_answer"],
                    explanation=question_data["explanation"],
                    difficulty=DifficultyLevel(question_data["difficulty"]),
                    points=question_data["points"],
                    subject=question_data["subject"],
                    tags=question_data["tags"],
                    exercise_id=exercise.id
                )

                question = self.exercise_service.create_question(question_create, teacher_id)
                saved_questions.append({
                    "id": question.id,
                    "title": question.title,
                    "type": question.question_type
                })

            return {
                "exercise_id": exercise.id,
                "exercise_title": exercise.title,
                "questions_count": len(saved_questions),
                "questions": saved_questions
            }

        except Exception as e:
            logger.error(f"保存习题失败: {str(e)}")
            return None

    def _generate_mock_course(self) -> Dict[str, Any]:
        """生成模拟课程数据"""
        return {
            "title": "基于知识库的示例课程",
            "description": "这是一个基于知识库内容生成的示例课程，包含多个学习模块。",
            "category": "综合",
            "difficulty": "medium",
            "duration": 480,
            "lessons": [
                {
                    "title": "课程导论",
                    "description": "课程概述和学习目标介绍",
                    "content": "本课程将带您深入了解相关知识点...",
                    "duration": 60,
                    "lesson_type": "text",
                    "lesson_order": 1,
                    "is_free": True
                },
                {
                    "title": "基础概念",
                    "description": "核心概念和基础理论",
                    "content": "在这一课时中，我们将学习基础概念...",
                    "duration": 60,
                    "lesson_type": "text",
                    "lesson_order": 2,
                    "is_free": False
                }
            ]
        }

    def _generate_mock_exercises(self) -> Dict[str, Any]:
        """生成模拟习题数据"""
        return {
            "exercise_title": "基于知识库的示例习题集",
            "exercise_description": "这是一个基于知识库内容生成的示例习题集。",
            "questions": [
                {
                    "title": "选择题示例",
                    "content": "以下哪个选项是正确的？",
                    "question_type": "multiple_choice",
                    "options": {
                        "A": "选项A",
                        "B": "选项B",
                        "C": "选项C",
                        "D": "选项D"
                    },
                    "correct_answer": "A",
                    "explanation": "正确答案是A，因为...",
                    "difficulty": "medium",
                    "points": 10,
                    "subject": "综合",
                    "tags": ["基础", "概念"]
                },
                {
                    "title": "填空题示例",
                    "content": "请填写空白处：______是重要的概念。",
                    "question_type": "fill_blank",
                    "options": None,
                    "correct_answer": "知识",
                    "explanation": "这里应该填入'知识'，因为...",
                    "difficulty": "medium",
                    "points": 10,
                    "subject": "综合",
                    "tags": ["基础", "填空"]
                }
            ]
        }

    def _generate_default_course(self, topic: str) -> Dict[str, Any]:
        """生成默认课程结构"""
        return {
            "title": f"{topic}课程",
            "description": f"关于{topic}的综合性课程",
            "category": "综合",
            "difficulty": "medium",
            "duration": 480,
            "lessons": [
                {
                    "title": f"{topic}概述",
                    "description": f"{topic}的基本介绍",
                    "content": f"本课时将介绍{topic}的基本概念和重要性。",
                    "duration": 60,
                    "lesson_type": "text",
                    "lesson_order": 1,
                    "is_free": True,
                    "is_published": False
                }
            ]
        }

    def _generate_default_exercises(self, topic: str) -> Dict[str, Any]:
        """生成默认习题结构"""
        return {
            "title": f"{topic}习题集",
            "description": f"关于{topic}的练习题目",
            "category": "自主练习",  # 使用正确的枚举值
            "subject": topic,
            "difficulty": "medium",
            "time_limit": 60,
            "course_id": None,
            "is_published": False,
            "questions": [
                {
                    "title": f"{topic}基础题",
                    "content": f"请简述{topic}的基本概念。",
                    "question_type": "essay",
                    "options": None,
                    "correct_answer": f"{topic}是一个重要的概念...",
                    "explanation": "这是一道开放性题目，答案可以从多个角度来回答。",
                    "difficulty": "medium",
                    "points": 10,
                    "subject": topic,
                    "tags": ["基础", "概念"]
                }
            ]
        }

    def _generate_knowledge_based_mock_exercises(self, topic: str, exercise_types: List[str], question_count: int) -> dict:
        """
        生成基于知识库内容的模拟习题
        当AI服务失败时的回退方案
        """
        logger.info(f"🔄 生成基于知识库的模拟习题: {topic}")

        # 根据题目类型生成不同的题目
        questions = []

        for i in range(question_count):
            question_type = exercise_types[i % len(exercise_types)] if exercise_types else "multiple_choice"

            if question_type == "multiple_choice":
                # 生成更有意义的选择题
                question_templates = [
                    {
                        "content": f"关于{topic}的基本概念，以下哪个说法是正确的？",
                        "options": [
                            f"{topic}是一种重要的技术概念，广泛应用于现代系统",
                            f"{topic}只适用于特定的应用场景，使用范围有限",
                            f"{topic}是过时的技术，现在已经不再使用",
                            f"{topic}只是理论概念，没有实际应用价值"
                        ],
                        "correct_answer": "A",
                        "explanation": f"根据{topic}的定义和广泛应用，选项A正确描述了{topic}的重要性和应用范围。"
                    },
                    {
                        "content": f"在实际应用中，{topic}的主要优势是什么？",
                        "options": [
                            f"提高系统效率和性能",
                            f"增加系统复杂度",
                            f"降低系统可靠性",
                            f"限制系统扩展性"
                        ],
                        "correct_answer": "A",
                        "explanation": f"{topic}的主要目标是提高系统效率和性能，这是其核心优势。"
                    },
                    {
                        "content": f"学习{topic}时，最重要的是掌握哪个方面？",
                        "options": [
                            f"基本原理和核心概念",
                            f"具体的实现细节",
                            f"历史发展过程",
                            f"相关的商业模式"
                        ],
                        "correct_answer": "A",
                        "explanation": f"学习{topic}时，首先要掌握基本原理和核心概念，这是理解和应用的基础。"
                    }
                ]

                template = question_templates[i % len(question_templates)]
                question = {
                    "title": f"{topic}选择题{i+1}",
                    "content": template["content"],
                    "question_type": "multiple_choice",
                    "options": template["options"],
                    "correct_answer": template["correct_answer"],
                    "explanation": template["explanation"],
                    "difficulty": "medium",
                    "points": 10,
                    "subject": topic,
                    "tags": ["基础", "选择题"]
                }
            elif question_type == "true_false":
                # 生成更有意义的判断题
                true_false_templates = [
                    {
                        "content": f"{topic}是现代信息技术的重要组成部分。",
                        "correct_answer": "正确",
                        "explanation": f"{topic}确实是现代信息技术体系中的重要组成部分。"
                    },
                    {
                        "content": f"学习{topic}需要具备扎实的理论基础。",
                        "correct_answer": "正确",
                        "explanation": f"掌握{topic}确实需要良好的理论基础作为支撑。"
                    },
                    {
                        "content": f"{topic}只能在特定环境下使用，适用性较差。",
                        "correct_answer": "错误",
                        "explanation": f"{topic}具有良好的适用性，可以在多种环境下使用。"
                    }
                ]

                template = true_false_templates[i % len(true_false_templates)]
                question = {
                    "title": f"{topic}判断题{i+1}",
                    "content": template["content"],
                    "question_type": "true_false",
                    "options": ["正确", "错误"],
                    "correct_answer": template["correct_answer"],
                    "explanation": template["explanation"],
                    "difficulty": "easy",
                    "points": 5,
                    "subject": topic,
                    "tags": ["基础", "判断题"]
                }
            elif question_type == "fill_blank":
                # 生成更有意义的填空题
                fill_blank_templates = [
                    {
                        "content": f"{topic}的主要目标是提高______和______。",
                        "correct_answer": "效率、性能",
                        "explanation": f"{topic}的核心目标是提高系统效率和性能。"
                    },
                    {
                        "content": f"在学习{topic}时，首先要掌握其______原理。",
                        "correct_answer": "基本",
                        "explanation": f"学习{topic}的第一步是理解其基本原理。"
                    },
                    {
                        "content": f"{topic}技术的发展趋势是向______化方向发展。",
                        "correct_answer": "智能",
                        "explanation": f"现代{topic}技术正朝着智能化方向发展。"
                    }
                ]

                template = fill_blank_templates[i % len(fill_blank_templates)]
                question = {
                    "title": f"{topic}填空题{i+1}",
                    "content": template["content"],
                    "question_type": "fill_blank",
                    "options": None,
                    "correct_answer": template["correct_answer"],
                    "explanation": template["explanation"],
                    "difficulty": "medium",
                    "points": 8,
                    "subject": topic,
                    "tags": ["基础", "填空题"]
                }
            else:  # essay
                # 生成更有意义的简答题
                essay_templates = [
                    {
                        "content": f"请分析{topic}的主要特点及其在现代应用中的重要性。",
                        "correct_answer": f"{topic}具有以下主要特点：1）高效性；2）可扩展性；3）可靠性。在现代应用中，{topic}发挥着重要作用，能够显著提升系统性能和用户体验。",
                        "explanation": "这道题考查对{topic}特点的理解和应用价值的认识。"
                    },
                    {
                        "content": f"结合实际案例，说明{topic}的应用场景和实施要点。",
                        "correct_answer": f"{topic}广泛应用于多个领域，如企业信息化、数据处理、系统优化等。实施时需要注意：1）需求分析；2）技术选型；3）实施规划；4）效果评估。",
                        "explanation": "这道题考查{topic}的实际应用能力和实施经验。"
                    }
                ]

                template = essay_templates[i % len(essay_templates)]
                question = {
                    "title": f"{topic}简答题{i+1}",
                    "content": template["content"],
                    "question_type": "essay",
                    "options": None,
                    "correct_answer": template["correct_answer"],
                    "explanation": template["explanation"],
                    "difficulty": "hard",
                    "points": 15,
                    "subject": topic,
                    "tags": ["基础", "简答题"]
                }

            questions.append(question)

        return {
            "exercise_title": f"{topic}习题集",
            "exercise_description": f"基于知识库内容生成的{topic}相关习题",
            "difficulty": "medium",
            "time_limit": question_count * 3,  # 每题3分钟
            "course_id": None,
            "is_published": False,
            "questions": questions
        }
