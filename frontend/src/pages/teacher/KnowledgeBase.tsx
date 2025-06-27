import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  Database,
  Upload,
  Search,
  Filter,
  BookOpen,
  FileText,
  Trash2,
  Eye,
  Download,
  Plus,
  Sparkles,
  BarChart3,
  Brain
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/components/ui/use-toast";
import { DocumentUpload } from "@/components/ui/DocumentUpload";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import TeacherLayout from "@/components/layouts/TeacherLayout";
import SemanticSearch from "@/components/SemanticSearch";
import {
  KnowledgeDocument,
  KnowledgeDocumentResponse,
  DOCUMENT_CATEGORIES,
  FILE_TYPE_ICONS,
  formatFileSize,
  formatUploadTime
} from "@/types/knowledge";
import KnowledgeAPI, { SemanticSearchResult } from "@/services/knowledgeAPI";

export const TeacherKnowledgeBase = () => {
  const { toast } = useToast();
  
  // 状态管理
  const [documents, setDocuments] = useState<KnowledgeDocument[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalDocuments, setTotalDocuments] = useState(0);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [showSearchResults, setShowSearchResults] = useState(false);
  const [activeTab, setActiveTab] = useState('documents');

  // 页面大小
  const pageSize = 12;

  // 获取文档列表
  const fetchDocuments = async (page: number = 1, category: string = '', search: string = '') => {
    try {
      setLoading(true);

      const data = await KnowledgeAPI.getDocuments(
        page,
        pageSize,
        category || undefined,
        search || undefined
      );

      setDocuments(data.documents);
      setTotalPages(data.pages);
      setTotalDocuments(data.total);
      setCurrentPage(data.page);

    } catch (error) {
      console.error('获取文档列表失败:', error);
      toast({
        title: "错误",
        description: error instanceof Error ? error.message : "获取文档列表失败，请重试",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  // 初始加载
  useEffect(() => {
    fetchDocuments();
  }, []);

  // 智能搜索和筛选
  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      setShowSearchResults(false);
      setCurrentPage(1);
      fetchDocuments(1, selectedCategory, '');
      return;
    }

    try {
      setIsSearching(true);

      // 使用专门的搜索API
      const results = await KnowledgeAPI.searchDocuments(searchQuery.trim(), 10);

      setSearchResults(results);
      setShowSearchResults(true);

      toast({
        title: "搜索完成",
        description: `找到 ${results.length} 个相关文档`
      });

    } catch (error) {
      console.error('搜索失败:', error);
      toast({
        title: "搜索失败",
        description: error instanceof Error ? error.message : "搜索失败，请重试",
        variant: "destructive"
      });
    } finally {
      setIsSearching(false);
    }
  };

  // 清除搜索结果
  const clearSearch = () => {
    setSearchQuery('');
    setSearchResults([]);
    setShowSearchResults(false);
    setCurrentPage(1);
    fetchDocuments(1, selectedCategory, '');
  };

  const handleCategoryChange = (category: string) => {
    const actualCategory = category === 'all' ? '' : category;
    setSelectedCategory(actualCategory);
    setCurrentPage(1);

    // 如果有搜索结果，清除搜索
    if (showSearchResults) {
      clearSearch();
    } else {
      fetchDocuments(1, actualCategory, '');
    }
  };

  // 文件上传处理
  const handleFileUpload = async (file: File, category: string = '教材', tags: string = '') => {
    try {
      console.log('开始上传文件:', file.name, '大小:', file.size, '类型:', file.type);
      setIsUploading(true);

      const result = await KnowledgeAPI.uploadDocument(file, category, tags);
      console.log('上传成功结果:', result);

      toast({
        title: "上传成功",
        description: `文档 "${file.name}" 已成功上传到知识库`
      });

      // 刷新文档列表
      fetchDocuments(currentPage, selectedCategory, searchQuery);
      setShowUploadModal(false);

    } catch (error) {
      console.error('文档上传失败:', error);
      toast({
        title: "上传失败",
        description: error instanceof Error ? error.message : "文档上传失败，请重试",
        variant: "destructive"
      });
    } finally {
      setIsUploading(false);
    }
  };

  // 删除文档
  const handleDeleteDocument = async (documentId: number, title: string) => {
    if (!confirm(`确定要删除文档 "${title}" 吗？此操作不可撤销。`)) {
      return;
    }

    try {
      await KnowledgeAPI.deleteDocument(documentId);

      toast({
        title: "删除成功",
        description: `文档 "${title}" 已从知识库中删除`
      });

      // 刷新文档列表
      fetchDocuments(currentPage, selectedCategory, searchQuery);

    } catch (error) {
      console.error('删除文档失败:', error);
      toast({
        title: "删除失败",
        description: error instanceof Error ? error.message : "删除文档失败，请重试",
        variant: "destructive"
      });
    }
  };

  // 计算统计信息
  const totalSize = documents.reduce((sum, doc) => sum + doc.file_size, 0);
  const categoryStats = DOCUMENT_CATEGORIES.map(cat => ({
    ...cat,
    count: documents.filter(doc => doc.category === cat.value).length
  }));

  return (
    <TeacherLayout>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6">
        {/* 页面标题 */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 flex items-center">
                <Database className="w-8 h-8 mr-3 text-blue-600" />
                我的知识库
              </h1>
              <p className="text-gray-600 mt-2">管理您的教学资料，让AI更好地为您服务</p>
            </div>
            
            <div className="flex items-center space-x-3">
              <Button
                onClick={() => setShowUploadModal(true)}
                className="flex items-center space-x-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
              >
                <Plus className="w-4 h-4" />
                <span>上传文档</span>
              </Button>
            </div>
          </div>
        </div>

        {/* 统计卡片 */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">总文档数</p>
                  <p className="text-2xl font-bold text-blue-600">{totalDocuments}</p>
                </div>
                <FileText className="w-8 h-8 text-blue-600" />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">总大小</p>
                  <p className="text-2xl font-bold text-green-600">{formatFileSize(totalSize)}</p>
                </div>
                <BarChart3 className="w-8 h-8 text-green-600" />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">本月上传</p>
                  <p className="text-2xl font-bold text-purple-600">
                    {documents.filter(doc => {
                      const uploadDate = new Date(doc.upload_time);
                      const now = new Date();
                      return uploadDate.getMonth() === now.getMonth() && 
                             uploadDate.getFullYear() === now.getFullYear();
                    }).length}
                  </p>
                </div>
                <Upload className="w-8 h-8 text-purple-600" />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">AI可用</p>
                  <p className="text-2xl font-bold text-orange-600">{documents.length}</p>
                </div>
                <Sparkles className="w-8 h-8 text-orange-600" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* 标签页导航 */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="mb-8">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="documents" className="flex items-center space-x-2">
              <FileText className="w-4 h-4" />
              <span>文档管理</span>
            </TabsTrigger>
            <TabsTrigger value="semantic-search" className="flex items-center space-x-2">
              <Brain className="w-4 h-4" />
              <span>AI语义搜索</span>
            </TabsTrigger>
          </TabsList>

          {/* 文档管理标签页 */}
          <TabsContent value="documents" className="space-y-6">
            {/* 搜索和筛选区域 */}
            <Card>
              <CardContent className="p-6">
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                  <Input
                    placeholder="搜索文档标题或内容..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                    className="pl-10 pr-10"
                    disabled={isSearching}
                  />
                  {searchQuery && (
                    <button
                      onClick={clearSearch}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                    >
                      ×
                    </button>
                  )}
                </div>
              </div>

              <Select value={selectedCategory} onValueChange={handleCategoryChange} disabled={isSearching}>
                <SelectTrigger className="w-48">
                  <SelectValue placeholder="选择分类" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">全部分类</SelectItem>
                  {DOCUMENT_CATEGORIES.map(cat => (
                    <SelectItem key={cat.value} value={cat.value}>
                      {cat.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              <Button
                onClick={handleSearch}
                disabled={isSearching}
                className="flex items-center space-x-2"
              >
                {isSearching ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>搜索中...</span>
                  </>
                ) : (
                  <>
                    <Search className="w-4 h-4" />
                    <span>搜索</span>
                  </>
                )}
              </Button>

              {showSearchResults && (
                <Button
                  variant="outline"
                  onClick={clearSearch}
                  className="flex items-center space-x-2"
                >
                  <span>清除搜索</span>
                </Button>
              )}
            </div>

            {/* 搜索结果提示 */}
            {showSearchResults && (
              <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm text-blue-700">
                  搜索 "{searchQuery}" 找到 {searchResults.length} 个结果
                  {searchResults.some(r => r.relevance_score) && (
                    <span className="ml-2 text-xs text-blue-600">
                      (按相关度排序)
                    </span>
                  )}
                </p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* 文档列表区域 */}
        {loading || isSearching ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <span className="ml-3 text-gray-600">
              {isSearching ? '搜索中...' : '加载中...'}
            </span>
          </div>
        ) : (showSearchResults ? searchResults : documents).length === 0 ? (
          <Card>
            <CardContent className="p-12 text-center">
              <Database className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                {showSearchResults ? '没有找到相关文档' : '知识库为空'}
              </h3>
              <p className="text-gray-500 mb-6">
                {showSearchResults
                  ? `搜索 "${searchQuery}" 没有找到匹配的文档，请尝试其他关键词`
                  : (selectedCategory ? '该分类下没有文档' : '还没有上传任何文档')
                }
              </p>
              {!showSearchResults && (
                <Button
                  onClick={() => setShowUploadModal(true)}
                  className="flex items-center space-x-2"
                >
                  <Plus className="w-4 h-4" />
                  <span>上传第一个文档</span>
                </Button>
              )}
            </CardContent>
          </Card>
        ) : (
          <>
            {/* 文档网格 */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
              {(showSearchResults ? searchResults : documents).map((doc) => (
                <DocumentCard
                  key={doc.id}
                  document={doc}
                  onDelete={() => handleDeleteDocument(doc.id, doc.title)}
                  searchQuery={showSearchResults ? searchQuery : undefined}
                  relevanceScore={doc.relevance_score}
                />
              ))}
            </div>

            {/* 分页 - 只在非搜索状态下显示 */}
            {!showSearchResults && totalPages > 1 && (
              <div className="flex items-center justify-center space-x-2">
                <Button
                  variant="outline"
                  onClick={() => {
                    const newPage = currentPage - 1;
                    setCurrentPage(newPage);
                    fetchDocuments(newPage, selectedCategory, searchQuery);
                  }}
                  disabled={currentPage === 1}
                >
                  上一页
                </Button>
                
                <span className="text-sm text-gray-600">
                  第 {currentPage} 页，共 {totalPages} 页
                </span>
                
                <Button
                  variant="outline"
                  onClick={() => {
                    const newPage = currentPage + 1;
                    setCurrentPage(newPage);
                    fetchDocuments(newPage, selectedCategory, searchQuery);
                  }}
                  disabled={currentPage === totalPages}
                >
                  下一页
                </Button>
              </div>
            )}
          </>
        )}
          </TabsContent>

          {/* AI语义搜索标签页 */}
          <TabsContent value="semantic-search" className="space-y-6">
            <SemanticSearch
              onResultClick={(result) => {
                // 处理搜索结果点击，可以跳转到文档详情或下载
                console.log('点击搜索结果:', result);
                // 这里可以添加跳转到文档详情的逻辑
              }}
            />
          </TabsContent>
        </Tabs>

        {/* 上传模态框 */}
        {showUploadModal && (
          <UploadModal
            isOpen={showUploadModal}
            onClose={() => setShowUploadModal(false)}
            onUpload={handleFileUpload}
            isUploading={isUploading}
          />
        )}
      </div>
    </TeacherLayout>
  );
};

// 文档卡片组件
interface DocumentCardProps {
  document: KnowledgeDocument;
  onDelete: () => void;
  searchQuery?: string;
  relevanceScore?: number;
}

const DocumentCard = ({ document, onDelete, searchQuery, relevanceScore }: DocumentCardProps) => {
  const categoryInfo = DOCUMENT_CATEGORIES.find(cat => cat.value === document.category);
  const fileIcon = FILE_TYPE_ICONS[document.file_type as keyof typeof FILE_TYPE_ICONS] || '📄';

  // 文本高亮函数
  const highlightText = (text: string, query?: string) => {
    if (!query || !text) return text;

    const regex = new RegExp(`(${query})`, 'gi');
    const parts = text.split(regex);

    return parts.map((part, index) =>
      regex.test(part) ? (
        <mark key={index} className="bg-yellow-200 px-1 rounded">
          {part}
        </mark>
      ) : part
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Card className="h-full hover:shadow-lg transition-shadow duration-200">
        <CardContent className="p-4">
          <div className="flex items-start justify-between mb-3">
            <div className="flex items-center space-x-2">
              <span className="text-2xl">{fileIcon}</span>
              <div className="flex-1 min-w-0">
                <h3 className="font-medium text-gray-900 truncate" title={document.title}>
                  {highlightText(document.title, searchQuery)}
                </h3>
                <p className="text-sm text-gray-500 truncate" title={document.filename}>
                  {document.filename}
                </p>
                {relevanceScore && (
                  <p className="text-xs text-blue-600 mt-1">
                    相关度: {relevanceScore.toFixed(1)}
                  </p>
                )}
              </div>
            </div>

            <div className="flex items-center space-x-1">
              <Button
                variant="ghost"
                size="sm"
                className="h-8 w-8 p-0 text-gray-400 hover:text-red-600"
                onClick={onDelete}
              >
                <Trash2 className="w-4 h-4" />
              </Button>
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Badge className={categoryInfo?.color || 'bg-gray-100 text-gray-800'}>
                {document.category}
              </Badge>
              <span className="text-xs text-gray-500">
                {formatFileSize(document.file_size)}
              </span>
            </div>

            {document.summary && (
              <p className="text-sm text-gray-600 line-clamp-2" title={document.summary}>
                {highlightText(document.summary, searchQuery)}
              </p>
            )}

            {document.tags && (
              <div className="flex flex-wrap gap-1">
                {document.tags.split(',').slice(0, 3).map((tag, index) => (
                  <span
                    key={index}
                    className="inline-block px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded"
                  >
                    {tag.trim()}
                  </span>
                ))}
              </div>
            )}

            <div className="pt-2 border-t border-gray-100">
              <p className="text-xs text-gray-500">
                上传于 {formatUploadTime(document.upload_time)}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

// 上传模态框组件
interface UploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onUpload: (file: File, category: string, tags: string) => void;
  isUploading: boolean;
}

const UploadModal = ({ isOpen, onClose, onUpload, isUploading }: UploadModalProps) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [category, setCategory] = useState('教材');
  const [tags, setTags] = useState('');

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
  };

  const handleUpload = () => {
    if (selectedFile) {
      onUpload(selectedFile, category, tags);
    }
  };

  const handleClose = () => {
    if (!isUploading) {
      setSelectedFile(null);
      setCategory('教材');
      setTags('');
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">上传文档到知识库</h2>
          <Button
            variant="ghost"
            onClick={handleClose}
            disabled={isUploading}
            className="h-8 w-8 p-0"
          >
            ×
          </Button>
        </div>

        <div className="space-y-6">
          {/* 文件上传区域 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              选择文档
            </label>
            <DocumentUpload
              onFileSelect={handleFileSelect}
              acceptedTypes={['.pdf', '.docx', '.doc']}
              maxSize={100 * 1024 * 1024}
            />
          </div>

          {/* 分类选择 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              文档分类
            </label>
            <Select value={category} onValueChange={setCategory}>
              <SelectTrigger>
                <SelectValue placeholder="选择分类" />
              </SelectTrigger>
              <SelectContent>
                {DOCUMENT_CATEGORIES.map(cat => (
                  <SelectItem key={cat.value} value={cat.value}>
                    {cat.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* 标签输入 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              标签 (可选)
            </label>
            <Input
              placeholder="输入标签，用逗号分隔，如：数学,高等数学,微积分"
              value={tags}
              onChange={(e) => setTags(e.target.value)}
            />
            <p className="text-xs text-gray-500 mt-1">
              标签有助于更好地组织和搜索您的文档
            </p>
          </div>

          {/* 操作按钮 */}
          <div className="flex items-center justify-end space-x-3 pt-4 border-t">
            <Button
              variant="outline"
              onClick={handleClose}
              disabled={isUploading}
            >
              取消
            </Button>
            <Button
              onClick={handleUpload}
              disabled={!selectedFile || isUploading}
              className="flex items-center space-x-2"
            >
              {isUploading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>上传中...</span>
                </>
              ) : (
                <>
                  <Upload className="w-4 h-4" />
                  <span>上传文档</span>
                </>
              )}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};
