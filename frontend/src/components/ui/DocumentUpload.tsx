import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, X, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { Button } from './button';
import { Progress } from './progress';
import { Alert, AlertDescription } from './alert';
import { Card, CardContent } from './card';

interface DocumentUploadProps {
  onFileSelect?: (file: File) => void;
  onUploadComplete?: (result: any) => void;
  onUploadError?: (error: string) => void;
  maxSize?: number; // 文件大小限制 (bytes)
  acceptedTypes?: string[]; // 接受的文件类型
  disabled?: boolean;
  className?: string;
}

interface UploadedFile {
  file: File;
  progress: number;
  status: 'uploading' | 'success' | 'error';
  error?: string;
  result?: any;
}

export const DocumentUpload: React.FC<DocumentUploadProps> = ({
  onFileSelect,
  onUploadComplete,
  onUploadError,
  maxSize = 100 * 1024 * 1024, // 100MB
  acceptedTypes = ['.pdf', '.docx', '.doc'],
  disabled = false,
  className = ''
}) => {
  const [uploadedFile, setUploadedFile] = useState<UploadedFile | null>(null);
  const [isDragActive, setIsDragActive] = useState(false);

  const onDrop = useCallback((acceptedFiles: File[], rejectedFiles: any[]) => {
    if (rejectedFiles.length > 0) {
      const rejection = rejectedFiles[0];
      let errorMessage = '文件上传失败';
      
      if (rejection.errors.some((e: any) => e.code === 'file-too-large')) {
        errorMessage = `文件大小超过限制 (${maxSize / (1024 * 1024)}MB)`;
      } else if (rejection.errors.some((e: any) => e.code === 'file-invalid-type')) {
        errorMessage = `不支持的文件格式。支持的格式: ${acceptedTypes.join(', ')}`;
      }
      
      onUploadError?.(errorMessage);
      return;
    }

    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      setUploadedFile({
        file,
        progress: 0,
        status: 'uploading'
      });
      
      onFileSelect?.(file);
      simulateUpload(file);
    }
  }, [maxSize, acceptedTypes, onFileSelect, onUploadError]);

  const { getRootProps, getInputProps, isDragActive: dropzoneActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    maxSize,
    multiple: false,
    disabled
  });

  // 模拟上传进度（实际项目中应该使用真实的上传API）
  const simulateUpload = async (file: File) => {
    try {
      // 模拟上传进度
      for (let progress = 0; progress <= 100; progress += 10) {
        await new Promise(resolve => setTimeout(resolve, 100));
        setUploadedFile(prev => prev ? { ...prev, progress } : null);
      }

      // 模拟成功结果
      const mockResult = {
        filename: file.name,
        size: file.size,
        type: file.type,
        uploadedAt: new Date().toISOString()
      };

      setUploadedFile(prev => prev ? {
        ...prev,
        status: 'success',
        progress: 100,
        result: mockResult
      } : null);

      onUploadComplete?.(mockResult);

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : '上传失败';
      setUploadedFile(prev => prev ? {
        ...prev,
        status: 'error',
        error: errorMessage
      } : null);
      onUploadError?.(errorMessage);
    }
  };

  const removeFile = () => {
    setUploadedFile(null);
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (filename: string) => {
    const extension = filename.split('.').pop()?.toLowerCase();
    return <File className="w-8 h-8 text-blue-500" />;
  };

  return (
    <div className={`space-y-4 ${className}`}>
      {/* 上传区域 */}
      {!uploadedFile && (
        <div
          {...getRootProps()}
          className={`
            border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
            ${dropzoneActive || isDragActive 
              ? 'border-blue-500 bg-blue-50' 
              : 'border-gray-300 hover:border-gray-400'
            }
            ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
          `}
        >
          <input {...getInputProps()} />
          <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
          <div className="space-y-2">
            <p className="text-lg font-medium text-gray-700">
              {dropzoneActive ? '释放文件以上传' : '拖拽文件到此处或点击选择'}
            </p>
            <p className="text-sm text-gray-500">
              支持 PDF、Word 文档，最大 {maxSize / (1024 * 1024)}MB
            </p>
            <Button 
              type="button" 
              variant="outline" 
              disabled={disabled}
              className="mt-4"
            >
              选择文件
            </Button>
          </div>
        </div>
      )}

      {/* 文件上传状态 */}
      {uploadedFile && (
        <Card>
          <CardContent className="p-4">
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0">
                {getFileIcon(uploadedFile.file.name)}
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-2">
                  <div>
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {uploadedFile.file.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {formatFileSize(uploadedFile.file.size)}
                    </p>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    {uploadedFile.status === 'uploading' && (
                      <Loader2 className="w-4 h-4 animate-spin text-blue-500" />
                    )}
                    {uploadedFile.status === 'success' && (
                      <CheckCircle className="w-4 h-4 text-green-500" />
                    )}
                    {uploadedFile.status === 'error' && (
                      <AlertCircle className="w-4 h-4 text-red-500" />
                    )}
                    
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={removeFile}
                      className="h-6 w-6 p-0"
                    >
                      <X className="w-4 h-4" />
                    </Button>
                  </div>
                </div>

                {/* 上传进度 */}
                {uploadedFile.status === 'uploading' && (
                  <div className="space-y-1">
                    <Progress value={uploadedFile.progress} className="h-2" />
                    <p className="text-xs text-gray-500">
                      上传中... {uploadedFile.progress}%
                    </p>
                  </div>
                )}

                {/* 成功状态 */}
                {uploadedFile.status === 'success' && (
                  <Alert className="mt-2">
                    <CheckCircle className="h-4 w-4" />
                    <AlertDescription>
                      文件上传成功！可以开始生成课程了。
                    </AlertDescription>
                  </Alert>
                )}

                {/* 错误状态 */}
                {uploadedFile.status === 'error' && (
                  <Alert variant="destructive" className="mt-2">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>
                      {uploadedFile.error || '上传失败，请重试'}
                    </AlertDescription>
                  </Alert>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* 支持格式说明 */}
      <div className="text-xs text-gray-500 space-y-1">
        <p>支持的文件格式：</p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li>PDF 文档 (.pdf)</li>
          <li>Word 文档 (.docx, .doc)</li>
        </ul>
        <p>文件大小限制：{maxSize / (1024 * 1024)}MB</p>
      </div>
    </div>
  );
};

export default DocumentUpload;
