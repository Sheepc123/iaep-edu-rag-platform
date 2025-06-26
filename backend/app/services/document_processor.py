"""
文档处理服务
用于解析PDF和Word文档内容
"""
import os
import tempfile
from typing import Optional, Dict, Any
from pathlib import Path
import logging

try:
    import PyPDF2
    from docx import Document
    import fitz  # PyMuPDF
except ImportError as e:
    logging.warning(f"文档处理库未安装: {e}")

from fastapi import HTTPException, status, UploadFile

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """文档处理器"""
    
    SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.doc'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    def validate_file(self, file: UploadFile) -> bool:
        """验证文件格式和大小"""
        # 检查文件扩展名
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in self.SUPPORTED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"不支持的文件格式。支持的格式: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )
        
        # 检查文件大小
        if hasattr(file, 'size') and file.size > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"文件大小超过限制 ({self.MAX_FILE_SIZE // (1024*1024)}MB)"
            )
        
        return True
    
    async def extract_text(self, file: UploadFile) -> Dict[str, Any]:
        """从文档中提取文本内容"""
        self.validate_file(file)
        
        # 保存临时文件
        temp_file_path = None
        try:
            # 创建临时文件
            temp_file_path = os.path.join(
                self.temp_dir, 
                f"temp_{file.filename}"
            )
            
            # 保存上传的文件
            with open(temp_file_path, "wb") as temp_file:
                content = await file.read()
                temp_file.write(content)
            
            # 根据文件类型提取文本
            file_extension = Path(file.filename).suffix.lower()
            
            if file_extension == '.pdf':
                text_content = self._extract_pdf_text(temp_file_path)
            elif file_extension in ['.docx', '.doc']:
                text_content = self._extract_docx_text(temp_file_path)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="不支持的文件格式"
                )
            
            return {
                "filename": file.filename,
                "file_type": file_extension,
                "text_content": text_content,
                "word_count": len(text_content.split()),
                "char_count": len(text_content)
            }
            
        except Exception as e:
            logger.error(f"文档处理失败: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"文档处理失败: {str(e)}"
            )
        finally:
            # 清理临时文件
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except Exception as e:
                    logger.warning(f"清理临时文件失败: {e}")
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """提取PDF文本内容"""
        text_content = ""
        
        try:
            # 尝试使用PyMuPDF (fitz)
            doc = fitz.open(file_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text_content += page.get_text()
            doc.close()
            
        except Exception as e:
            logger.warning(f"PyMuPDF提取失败，尝试PyPDF2: {e}")
            try:
                # 备用方案：使用PyPDF2
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text_content += page.extract_text()
            except Exception as e2:
                logger.error(f"PDF文本提取失败: {e2}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="PDF文件解析失败"
                )
        
        return text_content.strip()
    
    def _extract_docx_text(self, file_path: str) -> str:
        """提取Word文档文本内容"""
        try:
            doc = Document(file_path)
            text_content = ""
            
            # 提取段落文本
            for paragraph in doc.paragraphs:
                text_content += paragraph.text + "\n"
            
            # 提取表格文本
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        text_content += cell.text + " "
                    text_content += "\n"
            
            return text_content.strip()
            
        except Exception as e:
            logger.error(f"Word文档解析失败: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Word文档解析失败"
            )
    
    def get_document_summary(self, text_content: str) -> Dict[str, Any]:
        """获取文档摘要信息"""
        lines = text_content.split('\n')
        paragraphs = [line.strip() for line in lines if line.strip()]
        
        return {
            "total_lines": len(lines),
            "total_paragraphs": len(paragraphs),
            "word_count": len(text_content.split()),
            "char_count": len(text_content),
            "estimated_reading_time": max(1, len(text_content.split()) // 200)  # 假设每分钟200字
        }
