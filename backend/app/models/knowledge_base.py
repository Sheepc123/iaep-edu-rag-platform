"""
知识库数据模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class TeacherKnowledgeDoc(Base):
    """教师知识库文档表"""
    __tablename__ = "teacher_knowledge_docs"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(10), nullable=False)
    file_size = Column(Integer, nullable=False)
    text_content = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    tags = Column(String(500), nullable=True)
    upload_time = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default="active")

    # 关系
    teacher = relationship("User", back_populates="knowledge_docs")


# 在User模型中添加反向关系（需要在models/user.py中添加）
# knowledge_docs = relationship("TeacherKnowledgeDoc", back_populates="teacher")
