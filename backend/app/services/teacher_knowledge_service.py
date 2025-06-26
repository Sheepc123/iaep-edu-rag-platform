"""
教师知识库服务
"""
import os
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path

from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text, and_, or_

from app.models.knowledge_base import TeacherKnowledgeDoc
from app.schemas.knowledge_base import (
    KnowledgeDocumentCreate, KnowledgeDocument, KnowledgeDocumentList,
    KnowledgeSearchResult, UploadDocumentResponse
)
from app.services.document_processor import DocumentProcessor
from app.core.config import FileConfig


class TeacherKnowledgeService:
    """教师知识库服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.document_processor = DocumentProcessor()
        self.upload_dir = FileConfig.get_upload_dir()

        # 确保知识库上传目录存在
        self.knowledge_upload_dir = os.path.join(self.upload_dir, "knowledge_base")
        os.makedirs(self.knowledge_upload_dir, exist_ok=True)

        # 按年月创建子目录，便于管理
        from datetime import datetime
        current_date = datetime.now()
        self.current_month_dir = os.path.join(
            self.knowledge_upload_dir,
            f"{current_date.year:04d}",
            f"{current_date.month:02d}"
        )
        os.makedirs(self.current_month_dir, exist_ok=True)
    
    async def upload_document(self, file: UploadFile, teacher_id: int, 
                            category: str = "教材", tags: str = None) -> UploadDocumentResponse:
        """上传文档到教师知识库"""
        try:
            # 1. 验证文件
            self.document_processor.validate_file(file)
            
            # 2. 生成唯一文件名
            file_extension = Path(file.filename).suffix.lower()
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(self.current_month_dir, unique_filename)

            # 3. 重置文件指针并保存文件
            await file.seek(0)  # 重置文件指针
            content = await file.read()

            if len(content) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="上传的文件内容为空"
                )

            with open(file_path, "wb") as buffer:
                buffer.write(content)

            # 验证文件保存
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="文件保存失败"
                )
            
            # 4. 提取文本内容（重置文件指针）
            await file.seek(0)  # 再次重置文件指针用于文档处理
            document_info = await self.document_processor.extract_text(file)
            
            # 5. 生成文档标题（从文件名或内容中提取）
            title = self._extract_title(file.filename, document_info.get("text_content", ""))
            
            # 6. 生成摘要（可选）
            summary = self._generate_summary(document_info.get("text_content", ""))
            
            # 7. 保存到数据库
            doc_record = TeacherKnowledgeDoc(
                teacher_id=teacher_id,
                title=title,
                filename=file.filename,
                file_path=file_path,
                file_type=file_extension,
                file_size=len(content),
                text_content=document_info.get("text_content"),
                summary=summary,
                category=category,
                tags=tags,
                status="active"
            )
            
            self.db.add(doc_record)
            self.db.commit()
            self.db.refresh(doc_record)
            
            return UploadDocumentResponse(
                success=True,
                document_id=doc_record.id,
                message="文档上传成功"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            # 清理已保存的文件
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"文档上传失败: {str(e)}"
            )
    
    def get_teacher_documents(self, teacher_id: int, category: str = None, 
                            page: int = 1, size: int = 20) -> KnowledgeDocumentList:
        """获取教师的知识库文档列表"""
        try:
            # 构建查询
            query = self.db.query(TeacherKnowledgeDoc).filter(
                and_(
                    TeacherKnowledgeDoc.teacher_id == teacher_id,
                    TeacherKnowledgeDoc.status == 'active'
                )
            )
            
            if category:
                query = query.filter(TeacherKnowledgeDoc.category == category)
            
            # 按上传时间倒序排列
            query = query.order_by(TeacherKnowledgeDoc.upload_time.desc())
            
            # 分页
            total = query.count()
            documents = query.offset((page - 1) * size).limit(size).all()
            
            # 计算总页数
            pages = (total + size - 1) // size
            
            return KnowledgeDocumentList(
                documents=[self._format_document(doc) for doc in documents],
                total=total,
                page=page,
                size=size,
                pages=pages
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"获取文档列表失败: {str(e)}"
            )
    
    def search_documents(self, teacher_id: int, query: str, limit: int = 10) -> List[KnowledgeSearchResult]:
        """搜索教师知识库文档"""

        # 首先尝试FTS5搜索
        fts_results = self._search_with_fts5(teacher_id, query, limit)

        # 如果FTS5搜索结果较少且包含中文，尝试改进的中文搜索
        if len(fts_results) < 3 and self._contains_chinese(query):
            print(f"🔍 FTS5结果较少({len(fts_results)})，尝试中文优化搜索...")
            chinese_results = self._search_chinese_optimized(teacher_id, query, limit)

            # 合并结果，去重
            seen_ids = {result.id for result in fts_results}
            for result in chinese_results:
                if result.id not in seen_ids:
                    fts_results.append(result)
                    seen_ids.add(result.id)
                    if len(fts_results) >= limit:
                        break

        return fts_results[:limit]

    def _search_with_fts5(self, teacher_id: int, query: str, limit: int = 10) -> List[KnowledgeSearchResult]:
        """使用FTS5搜索"""
        try:
            # 使用SQLite FTS5全文搜索
            sql = text("""
            SELECT d.*,
                   bm25(teacher_knowledge_docs_fts) as rank
            FROM teacher_knowledge_docs d
            JOIN teacher_knowledge_docs_fts ON d.id = teacher_knowledge_docs_fts.rowid
            WHERE d.teacher_id = :teacher_id
            AND d.status = 'active'
            AND teacher_knowledge_docs_fts MATCH :query
            ORDER BY rank
            LIMIT :limit
            """)

            print(f"🔍 执行FTS5搜索: teacher_id={teacher_id}, query='{query}', limit={limit}")

            results = self.db.execute(sql, {
                "teacher_id": teacher_id,
                "query": query,
                "limit": limit
            }).fetchall()

            print(f"✅ FTS5搜索成功，找到 {len(results)} 个结果")
            
            search_results = []
            for result in results:
                # 尝试获取相关度评分
                try:
                    relevance_score = float(result.rank) if result.rank is not None else None
                except (AttributeError, ValueError, TypeError):
                    relevance_score = None

                search_results.append(KnowledgeSearchResult(
                    id=result.id,
                    title=result.title,
                    filename=result.filename,
                    category=result.category,
                    file_size=result.file_size,
                    upload_time=result.upload_time,
                    relevance_score=relevance_score
                ))
            
            return search_results

        except Exception as e:
            print(f"⚠️  FTS5搜索失败: {str(e)}")
            return []

    def _search_chinese_optimized(self, teacher_id: int, query: str, limit: int = 10) -> List[KnowledgeSearchResult]:
        """中文优化搜索"""
        try:
            # 对中文查询进行字符级别的搜索
            char_patterns = []
            for char in query:
                if self._is_chinese_char(char):
                    char_patterns.append(f"%{char}%")

            if not char_patterns:
                return []

            # 构建查询条件
            conditions = []
            for pattern in char_patterns:
                conditions.extend([
                    TeacherKnowledgeDoc.title.like(pattern),
                    TeacherKnowledgeDoc.text_content.like(pattern),
                    TeacherKnowledgeDoc.summary.like(pattern)
                ])

            results = self.db.query(TeacherKnowledgeDoc).filter(
                and_(
                    TeacherKnowledgeDoc.teacher_id == teacher_id,
                    TeacherKnowledgeDoc.status == 'active',
                    or_(*conditions)
                )
            ).order_by(TeacherKnowledgeDoc.upload_time.desc()).limit(limit).all()

            print(f"✅ 中文优化搜索成功，找到 {len(results)} 个结果")

            return [KnowledgeSearchResult(
                id=doc.id,
                title=doc.title,
                filename=doc.filename,
                category=doc.category,
                file_size=doc.file_size,
                upload_time=doc.upload_time,
                relevance_score=self._calculate_chinese_relevance(doc, query)
            ) for doc in results]

        except Exception as e:
            print(f"❌ 中文优化搜索失败: {str(e)}")
            return []

    def _contains_chinese(self, text: str) -> bool:
        """检查文本是否包含中文字符"""
        for char in text:
            if self._is_chinese_char(char):
                return True
        return False

    def _is_chinese_char(self, char: str) -> bool:
        """检查字符是否为中文字符"""
        return '\u4e00' <= char <= '\u9fff'

    def _calculate_chinese_relevance(self, doc: TeacherKnowledgeDoc, query: str) -> float:
        """计算中文搜索的相关度"""
        score = 0.0

        # 标题匹配权重更高
        if doc.title and query in doc.title:
            score += 10.0

        # 内容匹配
        if doc.text_content:
            # 计算查询词在内容中出现的次数
            content_lower = doc.text_content.lower()
            query_lower = query.lower()

            # 完整匹配
            if query_lower in content_lower:
                score += 5.0

            # 字符匹配
            for char in query:
                if self._is_chinese_char(char) and char in content_lower:
                    score += 1.0

        # 摘要匹配
        if doc.summary and query in doc.summary:
            score += 3.0

        return score
    
    def delete_document(self, document_id: int, teacher_id: int) -> bool:
        """删除文档 (软删除)"""
        try:
            doc = self.db.query(TeacherKnowledgeDoc).filter(
                and_(
                    TeacherKnowledgeDoc.id == document_id,
                    TeacherKnowledgeDoc.teacher_id == teacher_id
                )
            ).first()
            
            if not doc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="文档不存在"
                )
            
            # 软删除
            doc.status = 'deleted'
            self.db.commit()
            
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"删除文档失败: {str(e)}"
            )
    
    def get_document_content(self, document_id: int, teacher_id: int) -> str:
        """获取文档的文本内容"""
        try:
            doc = self.db.query(TeacherKnowledgeDoc).filter(
                and_(
                    TeacherKnowledgeDoc.id == document_id,
                    TeacherKnowledgeDoc.teacher_id == teacher_id,
                    TeacherKnowledgeDoc.status == 'active'
                )
            ).first()
            
            if not doc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="文档不存在"
                )
            
            return doc.text_content or ""
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"获取文档内容失败: {str(e)}"
            )
    
    def _extract_title(self, filename: str, content: str) -> str:
        """从文件名或内容中提取标题"""
        # 先尝试从文件名提取
        title = Path(filename).stem
        
        # 如果内容存在，尝试从内容的前几行提取更好的标题
        if content:
            lines = content.strip().split('\n')[:5]  # 取前5行
            for line in lines:
                line = line.strip()
                if line and len(line) < 100:  # 合理的标题长度
                    title = line
                    break
        
        return title[:255]  # 限制长度
    
    def _generate_summary(self, content: str) -> str:
        """生成文档摘要"""
        if not content:
            return ""
        
        # 简单的摘要生成：取前200个字符
        summary = content.strip()[:200]
        if len(content) > 200:
            summary += "..."
        
        return summary
    
    def _format_document(self, doc: TeacherKnowledgeDoc) -> KnowledgeDocument:
        """格式化文档对象"""
        return KnowledgeDocument(
            id=doc.id,
            teacher_id=doc.teacher_id,
            title=doc.title,
            filename=doc.filename,
            file_path=doc.file_path,
            file_type=doc.file_type,
            file_size=doc.file_size,
            text_content=doc.text_content,
            summary=doc.summary,
            category=doc.category,
            tags=doc.tags,
            upload_time=doc.upload_time,
            status=doc.status
        )
