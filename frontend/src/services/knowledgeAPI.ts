/**
 * 教师知识库API服务
 */

import { tokenManager } from './api';

// API基础URL
const API_BASE_URL = '/api/v1/teacher-knowledge';

// 获取认证头
const getAuthHeaders = () => {
  const token = tokenManager.getAccessToken();
  return {
    'Authorization': `Bearer ${token}`
  };
};

// 知识库文档接口
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
  status: string;
}

export interface KnowledgeDocumentList {
  documents: KnowledgeDocument[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface UploadDocumentResponse {
  success: boolean;
  document_id: number;
  message: string;
}

export interface KnowledgeSearchResult {
  id: number;
  title: string;
  filename: string;
  category: string;
  file_size: number;
  upload_time: string;
  relevance_score?: number;
}

export interface DeleteDocumentResponse {
  success: boolean;
  message: string;
}

export interface KnowledgeStats {
  total_documents: number;
  total_size: number;
  this_month_uploads: number;
  category_stats: Record<string, { count: number; size: number }>;
  avg_document_size: number;
}

// 语义搜索相关接口
export interface SemanticSearchRequest {
  query: string;
  top_k?: number;
  category?: string;
  tags?: string[];
}

export interface SemanticSearchResult {
  document_id: number;
  title: string;
  content: string;
  similarity: number;
  category?: string;
  tags?: string[];
  file_type?: string;
  enhanced_by?: string;
}

export interface VectorStats {
  available: boolean;
  stats?: {
    total_vectors: number;
    collection_name: string;
    embedding_model: string;
    embedding_dimension: number;
    enhancement: string;
  };
  message?: string;
}

export interface DocumentCategory {
  value: string;
  label: string;
  description: string;
}

// 知识库API类
export class KnowledgeAPI {
  
  /**
   * 上传文档到知识库
   */
  static async uploadDocument(
    file: File, 
    category: string = '教材', 
    tags: string = ''
  ): Promise<UploadDocumentResponse> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('category', category);
    formData.append('tags', tags);

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: formData
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`文档上传失败: ${response.status} - ${errorText}`);
    }

    return await response.json();
  }

  /**
   * 获取文档列表
   */
  static async getDocuments(
    page: number = 1,
    size: number = 20,
    category?: string,
    search?: string
  ): Promise<KnowledgeDocumentList> {
    const params = new URLSearchParams({
      page: page.toString(),
      size: size.toString()
    });
    
    if (category) params.append('category', category);
    if (search) params.append('search', search);

    const response = await fetch(`${API_BASE_URL}/documents?${params}`, {
      headers: getAuthHeaders()
    });

    if (!response.ok) {
      throw new Error(`获取文档列表失败: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * 搜索文档
   */
  static async searchDocuments(
    query: string,
    limit: number = 10
  ): Promise<KnowledgeSearchResult[]> {
    const response = await fetch(`${API_BASE_URL}/search`, {
      method: 'POST',
      headers: {
        ...getAuthHeaders(),
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query, limit })
    });

    if (!response.ok) {
      throw new Error(`搜索文档失败: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * 删除文档
   */
  static async deleteDocument(documentId: number): Promise<DeleteDocumentResponse> {
    const response = await fetch(`${API_BASE_URL}/documents/${documentId}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });

    if (!response.ok) {
      throw new Error(`删除文档失败: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * 获取文档内容
   */
  static async getDocumentContent(documentId: number): Promise<{ document_id: number; content: string }> {
    const response = await fetch(`${API_BASE_URL}/documents/${documentId}/content`, {
      headers: getAuthHeaders()
    });

    if (!response.ok) {
      throw new Error(`获取文档内容失败: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * 获取文档分类列表
   */
  static async getCategories(): Promise<{ categories: DocumentCategory[] }> {
    const response = await fetch(`${API_BASE_URL}/categories`, {
      headers: getAuthHeaders()
    });

    if (!response.ok) {
      throw new Error(`获取分类列表失败: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * 获取知识库统计信息
   */
  static async getStats(): Promise<KnowledgeStats> {
    const response = await fetch(`${API_BASE_URL}/stats`, {
      headers: getAuthHeaders()
    });

    if (!response.ok) {
      throw new Error(`获取统计信息失败: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * DeepSeek语义搜索
   */
  static async semanticSearch(request: SemanticSearchRequest): Promise<SemanticSearchResult[]> {
    const response = await fetch(`${API_BASE_URL}/semantic-search`, {
      method: 'POST',
      headers: {
        ...getAuthHeaders(),
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request)
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`语义搜索失败: ${response.status} - ${errorText}`);
    }

    return await response.json();
  }

  /**
   * 获取向量数据库统计信息
   */
  static async getVectorStats(): Promise<VectorStats> {
    const response = await fetch(`${API_BASE_URL}/vector-stats`, {
      headers: getAuthHeaders()
    });

    if (!response.ok) {
      throw new Error(`获取向量统计失败: ${response.status}`);
    }

    return await response.json();
  }
}

// 导出默认实例
export default KnowledgeAPI;
