import React from 'react';
import { DocumentUpload } from './DocumentUpload';

// Simple test component to verify imports work
const TestDocumentUpload: React.FC = () => {
  const handleFileSelect = (file: File) => {
    console.log('File selected:', file.name);
  };

  const handleUploadComplete = (result: any) => {
    console.log('Upload complete:', result);
  };

  const handleUploadError = (error: string) => {
    console.error('Upload error:', error);
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Document Upload Test</h2>
      <DocumentUpload
        onFileSelect={handleFileSelect}
        onUploadComplete={handleUploadComplete}
        onUploadError={handleUploadError}
        maxSize={5 * 1024 * 1024} // 5MB
        acceptedTypes={['.pdf', '.docx', '.doc']}
      />
    </div>
  );
};

export default TestDocumentUpload;
