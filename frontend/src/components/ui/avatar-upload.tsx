import React, { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/use-toast';
import { Upload, Camera, X, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface AvatarUploadProps {
  currentAvatar: string;
  onAvatarChange: (avatarUrl: string) => void;
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
}

export const AvatarUpload: React.FC<AvatarUploadProps> = ({
  currentAvatar,
  onAvatarChange,
  size = 'md',
  disabled = false
}) => {
  const [isUploading, setIsUploading] = useState(false);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  // 尺寸配置
  const sizeConfig = {
    sm: { container: 'w-16 h-16', button: 'w-6 h-6', icon: 'w-3 h-3' },
    md: { container: 'w-32 h-32', button: 'w-8 h-8', icon: 'w-4 h-4' },
    lg: { container: 'w-40 h-40', button: 'w-10 h-10', icon: 'w-5 h-5' }
  };

  const config = sizeConfig[size];

  // 处理文件选择
  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // 验证文件类型
    if (!file.type.startsWith('image/')) {
      toast({
        title: "文件类型错误",
        description: "请选择图片文件",
        variant: "destructive",
      });
      return;
    }

    // 验证文件大小 (5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast({
        title: "文件过大",
        description: "图片大小不能超过5MB",
        variant: "destructive",
      });
      return;
    }

    // 创建预览URL
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    setShowUploadModal(true);
  };

  // 上传头像
  const handleUpload = async (file: File) => {
    setIsUploading(true);
    try {
      // 创建FormData
      const formData = new FormData();
      formData.append('avatar', file);

      // 调用上传API
      const response = await fetch('/api/v1/users/upload-avatar', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: formData
      });

      if (!response.ok) {
        throw new Error('上传失败');
      }

      const result = await response.json();
      
      // 更新头像URL
      onAvatarChange(result.avatar_url);
      
      toast({
        title: "上传成功",
        description: "头像已更新",
      });

      setShowUploadModal(false);
      setPreviewUrl(null);

    } catch (error) {
      console.error('头像上传失败:', error);
      toast({
        title: "上传失败",
        description: "请稍后重试",
        variant: "destructive",
      });
    } finally {
      setIsUploading(false);
    }
  };

  // 确认上传
  const confirmUpload = () => {
    const file = fileInputRef.current?.files?.[0];
    if (file) {
      handleUpload(file);
    }
  };

  // 取消上传
  const cancelUpload = () => {
    setShowUploadModal(false);
    setPreviewUrl(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <>
      {/* 头像显示区域 */}
      <div className="relative inline-block">
        <img
          src={currentAvatar}
          alt="用户头像"
          className={`${config.container} rounded-full border-4 border-white shadow-lg object-cover`}
        />
        
        {/* 编辑按钮 */}
        <Button
          size="sm"
          disabled={disabled}
          onClick={() => fileInputRef.current?.click()}
          className={`absolute bottom-2 right-2 rounded-full ${config.button} p-0 bg-blue-600 hover:bg-blue-700 disabled:opacity-50`}
        >
          <Camera className={config.icon} />
        </Button>

        {/* 隐藏的文件输入 */}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileSelect}
          className="hidden"
        />
      </div>

      {/* 上传确认模态框 */}
      <AnimatePresence>
        {showUploadModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={cancelUpload}
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              className="bg-white rounded-lg shadow-xl max-w-md w-full p-6"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold">更换头像</h3>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={cancelUpload}
                  className="p-1"
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>

              {/* 预览图片 */}
              {previewUrl && (
                <div className="flex justify-center mb-6">
                  <img
                    src={previewUrl}
                    alt="头像预览"
                    className="w-32 h-32 rounded-full object-cover border-4 border-gray-200"
                  />
                </div>
              )}

              {/* 操作按钮 */}
              <div className="flex space-x-3">
                <Button
                  variant="outline"
                  onClick={cancelUpload}
                  disabled={isUploading}
                  className="flex-1"
                >
                  取消
                </Button>
                <Button
                  onClick={confirmUpload}
                  disabled={isUploading}
                  className="flex-1 bg-blue-600 hover:bg-blue-700"
                >
                  {isUploading ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      上传中...
                    </>
                  ) : (
                    <>
                      <Upload className="w-4 h-4 mr-2" />
                      确认上传
                    </>
                  )}
                </Button>
              </div>

              {/* 上传提示 */}
              <div className="mt-4 text-sm text-gray-500 text-center">
                <p>支持 JPG、PNG、GIF 格式</p>
                <p>文件大小不超过 5MB</p>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};
