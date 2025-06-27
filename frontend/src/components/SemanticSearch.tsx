import React, { useState, useEffect } from 'react';
import {
  Search,
  Brain,
  FileText,
  Sparkles,
  AlertCircle,
  Loader2,
  TrendingUp
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import KnowledgeAPI from '@/services/knowledgeAPI';

// 类型定义
interface SemanticSearchResult {
  document_id: number;
  title: string;
  content: string;
  similarity: number;
  category?: string;
  tags?: string[];
  file_type?: string;
  enhanced_by?: string;
}

interface VectorStats {
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

interface SemanticSearchProps {
  onResultClick?: (result: SemanticSearchResult) => void;
}

const SemanticSearch: React.FC<SemanticSearchProps> = ({ onResultClick }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SemanticSearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [vectorStats, setVectorStats] = useState<VectorStats | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [topK, setTopK] = useState(5);

  // 获取向量统计信息
  useEffect(() => {
    const fetchVectorStats = async () => {
      try {
        const stats = await KnowledgeAPI.getVectorStats();
        setVectorStats(stats);
      } catch (err) {
        console.error('获取向量统计失败:', err);
      }
    };

    fetchVectorStats();
  }, []);

  // 执行语义搜索
  const handleSearch = async () => {
    if (!query.trim()) {
      setError('请输入搜索内容');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const searchRequest = {
        query: query.trim(),
        top_k: topK,
        ...(selectedCategory && selectedCategory !== 'all' && { category: selectedCategory })
      };

      const searchResults = await KnowledgeAPI.semanticSearch(searchRequest);
      setResults(searchResults);

      if (searchResults.length === 0) {
        setError('没有找到相关文档，请尝试其他关键词');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '搜索失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  // 处理回车键搜索
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  // 格式化相似度分数
  const formatSimilarity = (similarity: number) => {
    return (similarity * 100).toFixed(1);
  };

  // 获取相似度颜色
  const getSimilarityColor = (similarity: number) => {
    if (similarity >= 0.7) return 'text-green-600';
    if (similarity >= 0.4) return 'text-yellow-600';
    return 'text-red-600';
  };

  // 截断文本
  const truncateText = (text: string, maxLength: number = 150) => {
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
  };

  return (
    <div className="space-y-6">
      {/* 标题和状态 */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Brain className="h-6 w-6 text-blue-600" />
          <h2 className="text-2xl font-bold">DeepSeek 语义搜索</h2>
          <Sparkles className="h-5 w-5 text-yellow-500" />
        </div>
        
        {vectorStats && (
          <div className="text-sm text-gray-600">
            {vectorStats.available ? (
              <span className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span>已索引 {vectorStats.stats?.total_vectors || 0} 个文档块</span>
              </span>
            ) : (
              <span className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                <span>向量服务不可用</span>
              </span>
            )}
          </div>
        )}
      </div>

      {/* 搜索区域 */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">智能语义搜索</CardTitle>
          <p className="text-sm text-gray-600">
            使用 AI 理解您的查询意图，找到最相关的文档内容
          </p>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* 搜索输入 */}
          <div className="flex space-x-2">
            <div className="flex-1">
              <Input
                placeholder="输入您想要搜索的内容，例如：机器学习算法、Python编程..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                className="text-base"
              />
            </div>
            <Button 
              onClick={handleSearch} 
              disabled={loading || !vectorStats?.available}
              className="px-6"
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Search className="h-4 w-4" />
              )}
              搜索
            </Button>
          </div>

          {/* 搜索选项 */}
          <div className="flex space-x-4">
            <div className="flex items-center space-x-2">
              <label className="text-sm font-medium">分类:</label>
              <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                <SelectTrigger className="w-32">
                  <SelectValue placeholder="全部" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">全部</SelectItem>
                  <SelectItem value="教材">教材</SelectItem>
                  <SelectItem value="课件">课件</SelectItem>
                  <SelectItem value="论文">论文</SelectItem>
                  <SelectItem value="资料">资料</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-center space-x-2">
              <label className="text-sm font-medium">结果数:</label>
              <Select value={topK.toString()} onValueChange={(value) => setTopK(parseInt(value))}>
                <SelectTrigger className="w-20">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="3">3</SelectItem>
                  <SelectItem value="5">5</SelectItem>
                  <SelectItem value="10">10</SelectItem>
                  <SelectItem value="20">20</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* 错误提示 */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* 搜索结果 */}
      {results.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">搜索结果</h3>
            <span className="text-sm text-gray-600">找到 {results.length} 个相关文档</span>
          </div>

          {results.map((result, index) => (
            <Card 
              key={`${result.document_id}-${index}`}
              className="hover:shadow-md transition-shadow cursor-pointer"
              onClick={() => onResultClick?.(result)}
            >
              <CardContent className="p-4">
                <div className="space-y-3">
                  {/* 标题和相似度 */}
                  <div className="flex items-start justify-between">
                    <h4 className="font-semibold text-lg text-blue-700 hover:text-blue-800">
                      {result.title}
                    </h4>
                    <div className="flex items-center space-x-2">
                      <TrendingUp className="h-4 w-4 text-gray-400" />
                      <span className={`font-medium ${getSimilarityColor(result.similarity)}`}>
                        {formatSimilarity(result.similarity)}%
                      </span>
                    </div>
                  </div>

                  {/* 内容预览 */}
                  <p className="text-gray-700 leading-relaxed">
                    {truncateText(result.content)}
                  </p>

                  {/* 元数据 */}
                  <div className="flex items-center space-x-4 text-sm text-gray-500">
                    {result.category && (
                      <div className="flex items-center space-x-1">
                        <FileText className="h-4 w-4" />
                        <span>{result.category}</span>
                      </div>
                    )}
                    
                    {result.file_type && (
                      <Badge variant="outline" className="text-xs">
                        {result.file_type.toUpperCase()}
                      </Badge>
                    )}

                    {result.enhanced_by && (
                      <div className="flex items-center space-x-1">
                        <Sparkles className="h-3 w-3 text-yellow-500" />
                        <span className="text-xs">AI增强</span>
                      </div>
                    )}

                    {result.tags && result.tags.length > 0 && (
                      <div className="flex items-center space-x-1">
                        <Tag className="h-4 w-4" />
                        <div className="flex space-x-1">
                          {result.tags.slice(0, 3).map((tag, tagIndex) => (
                            <Badge key={tagIndex} variant="secondary" className="text-xs">
                              {tag}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* 向量服务信息 */}
      {vectorStats?.available && vectorStats.stats && (
        <Card className="bg-blue-50">
          <CardContent className="p-4">
            <div className="text-sm text-blue-800">
              <div className="font-medium mb-2">AI 搜索引擎信息</div>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div>模型: {vectorStats.stats.embedding_model}</div>
                <div>增强: {vectorStats.stats.enhancement}</div>
                <div>维度: {vectorStats.stats.embedding_dimension}</div>
                <div>集合: {vectorStats.stats.collection_name}</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default SemanticSearch;
