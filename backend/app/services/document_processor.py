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
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    
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
            # 重置文件指针到开始位置
            await file.seek(0)

            # 创建临时文件，使用UUID避免中文路径问题
            import uuid
            file_extension = Path(file.filename).suffix.lower()
            temp_filename = f"temp_{uuid.uuid4().hex}{file_extension}"
            temp_file_path = os.path.join(self.temp_dir, temp_filename)

            # 读取文件内容
            content = await file.read()
            logger.info(f"读取文件内容，大小: {len(content)} bytes")

            if len(content) == 0:
                raise ValueError("上传的文件内容为空")

            # 保存上传的文件
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(content)

            # 验证文件是否正确保存
            if not os.path.exists(temp_file_path):
                raise FileNotFoundError("临时文件保存失败")

            saved_size = os.path.getsize(temp_file_path)
            logger.info(f"临时文件保存成功: {temp_file_path}, 大小: {saved_size} bytes")

            if saved_size == 0:
                raise ValueError("临时文件保存后为空")
            
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
            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"临时文件不存在: {file_path}")

            # 检查文件大小
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                raise ValueError("文件为空")

            logger.info(f"开始解析PDF文档: {file_path}, 大小: {file_size} bytes")

            # 尝试使用PyMuPDF (fitz)
            doc = fitz.open(file_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text_content += page.get_text()
            doc.close()

            logger.info(f"PDF文档解析成功，提取文本长度: {len(text_content)} 字符")

        except Exception as e:
            logger.warning(f"PyMuPDF提取失败，尝试PyPDF2: {e}")
            try:
                # 备用方案：使用PyPDF2
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text_content += page.extract_text()

                logger.info(f"PyPDF2解析成功，提取文本长度: {len(text_content)} 字符")

            except Exception as e2:
                logger.error(f"PDF文本提取失败: {e2}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="PDF文件解析失败，请检查文件是否为有效的PDF格式"
                )

        result = text_content.strip()
        if not result:
            logger.warning("PDF文档解析成功但未提取到文本内容")
            return "PDF文档内容为空或无法提取文本"

        return result
    
    def _extract_docx_text(self, file_path: str) -> str:
        """提取Word文档文本内容"""
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"临时文件不存在: {file_path}")

            # 检查文件大小
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                raise ValueError("文件为空")

            logger.info(f"开始解析Word文档: {file_path}, 大小: {file_size} bytes")

            doc = Document(file_path)
            text_content = ""

            # 提取段落文本
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_content += paragraph.text + "\n"

            # 提取表格文本
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if cell.text.strip():
                            text_content += cell.text + " "
                    text_content += "\n"

            result = text_content.strip()
            logger.info(f"Word文档解析成功，提取文本长度: {len(result)} 字符")

            if not result:
                logger.warning("Word文档解析成功但未提取到文本内容")
                return "文档内容为空或无法提取文本"

            return result

        except Exception as e:
            logger.error(f"Word文档解析失败: {e}")
            logger.error(f"文件路径: {file_path}")
            logger.error(f"文件是否存在: {os.path.exists(file_path) if file_path else 'N/A'}")

            # 返回更友好的错误信息
            if "Package not found" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Word文档格式错误或文件损坏，请检查文件是否为有效的.docx格式"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Word文档解析失败: {str(e)}"
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
