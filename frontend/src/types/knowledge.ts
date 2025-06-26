/**
 * 知识库相关类型定义
 */

export interface KnowledgeDocument {
  id: number;
  teacher_id: number;
  title: string;
  filename: string;
  file_path: string;
  file_type: string;
  file_size: number;
  text_content?: string;
  summary?: string;
  category: string;
  tags?: string;
  upload_time: string;
  status: 'active' | 'deleted';
}

export interface KnowledgeDocumentCreate {
  title?: string;
  category: string;
  tags?: string;
}

export interface KnowledgeDocumentResponse {
  documents: KnowledgeDocument[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface KnowledgeSearchResult {
  id: number;
  title: string;
  filename: string;
  category: string;
  file_size: number;
  upload_time: string;
  relevance_score?: number;
  matched_content?: string;
}

export interface UploadDocumentRequest {
  file: File;
  category: string;
  tags?: string;
}

export interface UploadDocumentResponse {
  success: boolean;
  document_id: number;
  message: string;
}

// 文档分类选项
export const DOCUMENT_CATEGORIES = [
  { value: '教材', label: '教材', color: 'bg-blue-100 text-blue-800' },
  { value: '参考书', label: '参考书', color: 'bg-green-100 text-green-800' },
  { value: '论文', label: '论文', color: 'bg-purple-100 text-purple-800' },
  { value: '课件', label: '课件', color: 'bg-orange-100 text-orange-800' },
  { value: '习题集', label: '习题集', color: 'bg-red-100 text-red-800' },
  { value: '其他', label: '其他', color: 'bg-gray-100 text-gray-800' }
] as const;

// 文件类型图标映射
export const FILE_TYPE_ICONS = {
  '.pdf': '📄',
  '.docx': '📝',
  '.doc': '📝',
  '.txt': '📄',
  '.md': '📄'
} as const;

// 格式化文件大小
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// 格式化上传时间
export const formatUploadTime = (dateString: string): string => {
  const date = new Date(dateString);
  const now = new Date();
  const diffTime = Math.abs(now.getTime() - date.getTime());
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  if (diffDays === 1) {
    return '今天';
  } else if (diffDays <= 7) {
    return `${diffDays} 天前`;
  } else {
    return date.toLocaleDateString('zh-CN');
  }
};
