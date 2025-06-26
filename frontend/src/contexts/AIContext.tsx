import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { aiAPI, AIMessage, AIConversation, AIMessageRequest } from '../services/api';

export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  type?: 'text' | 'suggestion' | 'exercise';
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  lastUpdated: Date;
}

interface AIContextType {
  conversations: Conversation[];
  currentConversationId: string;
  currentMessages: Message[];
  isTyping: boolean;
  setConversations: React.Dispatch<React.SetStateAction<Conversation[]>>;
  setCurrentConversationId: React.Dispatch<React.SetStateAction<string>>;
  setCurrentMessages: React.Dispatch<React.SetStateAction<Message[]>>;
  setIsTyping: React.Dispatch<React.SetStateAction<boolean>>;
  addMessage: (message: Message) => void;
  createNewConversation: () => string;
  switchConversation: (conversationId: string) => Promise<void>;
  deleteConversation: (conversationId: string) => Promise<void>;
  updateConversationTitle: (conversationId: string, title: string) => void;
  sendMessageToAPI: (content: string, conversationId?: string) => Promise<void>;
  loadConversations: () => Promise<void>;
}

const AIContext = createContext<AIContextType | undefined>(undefined);

export const useAI = () => {
  const context = useContext(AIContext);
  if (context === undefined) {
    throw new Error('useAI must be used within an AIProvider');
  }
  return context;
};

interface AIProviderProps {
  children: ReactNode;
}

export const AIProvider: React.FC<AIProviderProps> = ({ children }) => {
  const [conversations, setConversations] = useState<Conversation[]>([]);

  const [currentConversationId, setCurrentConversationId] = useState<string>('');
  const [currentMessages, setCurrentMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);

  const addMessage = (message: Message) => {
    const newMessages = [...currentMessages, message];
    setCurrentMessages(newMessages);
    
    // 更新对话记录
    setConversations(prev => prev.map(conv => {
      if (conv.id === currentConversationId) {
        return {
          ...conv,
          messages: newMessages,
          lastUpdated: new Date(),
          title: conv.title === '新对话' && message.sender === 'user' 
            ? message.content.slice(0, 20) + (message.content.length > 20 ? '...' : '')
            : conv.title
        };
      }
      return conv;
    }));
  };

  const createNewConversation = (): string => {
    const newConversation: Conversation = {
      id: Date.now().toString(),
      title: '新对话',
      messages: [
        {
          id: Date.now().toString(),
          content: '你好！我是你的AI学习助手小智，我可以帮助你：\n\n📚 解答学习问题\n🎯 制定学习计划\n📊 分析学习进度\n💡 提供学习建议\n\n有什么可以帮助你的吗？',
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        }
      ],
      lastUpdated: new Date()
    };
    
    setConversations(prev => [newConversation, ...prev]);
    setCurrentConversationId(newConversation.id);
    setCurrentMessages(newConversation.messages);
    
    return newConversation.id;
  };

  const switchConversation = async (conversationId: string) => {
    const conversation = conversations.find(c => c.id === conversationId);
    if (conversation) {
      setCurrentConversationId(conversationId);
      // 总是从服务器重新加载消息，确保数据是最新的
      await loadConversationMessages(conversationId);
    }
  };

  const deleteConversation = async (conversationId: string) => {
    if (conversations.length <= 1) return; // 至少保留一个对话

    try {
      // 调用后端API删除对话
      await aiAPI.deleteConversation(conversationId);

      // 前端状态更新
      const updatedConversations = conversations.filter(c => c.id !== conversationId);
      setConversations(updatedConversations);

      if (currentConversationId === conversationId) {
        const firstConversation = updatedConversations[0];
        setCurrentConversationId(firstConversation.id);
        setCurrentMessages(firstConversation.messages);
      }

      console.log('✅ 对话删除成功:', conversationId);
    } catch (error) {
      console.error('❌ 删除对话失败:', error);
      // 可以添加错误提示
      throw error;
    }
  };

  const updateConversationTitle = (conversationId: string, title: string) => {
    setConversations(prev => prev.map(conv => {
      if (conv.id === conversationId) {
        return { ...conv, title };
      }
      return conv;
    }));
  };

  // 从后端加载对话列表
  const loadConversations = async () => {
    try {
      console.log('开始加载对话列表...');
      console.log('当前token:', localStorage.getItem('access_token') ? '已存在' : '不存在');

      const apiConversations = await aiAPI.getConversations();
      console.log('成功获取对话列表:', apiConversations.length, '个对话');

      const formattedConversations: Conversation[] = apiConversations.map(conv => ({
        id: conv.id.toString(),
        title: conv.title,
        messages: [], // 消息将在切换对话时加载
        lastUpdated: new Date(conv.updated_at || conv.created_at)
      }));

      if (formattedConversations.length > 0) {
        setConversations(formattedConversations);
        // 加载第一个对话的消息
        await loadConversationMessages(formattedConversations[0].id);
        setCurrentConversationId(formattedConversations[0].id);
      } else {
        console.log('没有找到对话，将创建新对话');
      }
    } catch (error) {
      console.error('加载对话列表失败:', error);
      // 如果是认证错误，可能需要重新登录
      if (error.message && error.message.includes('401')) {
        console.error('认证失败，可能需要重新登录');
      }
    }
  };

  // 加载对话消息
  const loadConversationMessages = async (conversationId: string) => {
    try {
      const apiMessages = await aiAPI.getConversationMessages(conversationId);
      const formattedMessages: Message[] = apiMessages.map(msg => ({
        id: msg.id.toString(),
        content: msg.content,
        sender: msg.sender,
        timestamp: new Date(msg.created_at),
        type: msg.message_type as any
      }));

      setCurrentMessages(formattedMessages);

      // 更新对话中的消息
      setConversations(prev => prev.map(conv => {
        if (conv.id === conversationId) {
          return { ...conv, messages: formattedMessages };
        }
        return conv;
      }));
    } catch (error) {
      console.error('加载对话消息失败:', error);
    }
  };

  // 发送消息到API
  const sendMessageToAPI = async (content: string, conversationId?: string) => {
    try {
      console.log('开始发送消息到API:', content);
      console.log('使用对话ID:', conversationId || currentConversationId);
      console.log('当前token状态:', localStorage.getItem('access_token') ? '已存在' : '不存在');

      // 立即显示用户消息
      const userMessage: Message = {
        id: `temp-${Date.now()}`, // 临时ID
        content,
        sender: 'user',
        timestamp: new Date(),
        type: 'text'
      };
      addMessage(userMessage);

      setIsTyping(true);

      // 发送到后端API
      const messageRequest: AIMessageRequest = {
        content,
        message_type: 'text'
      };

      // 只有当有有效的对话ID时才添加conversation_id
      const targetConversationId = conversationId || currentConversationId;
      if (targetConversationId && targetConversationId.trim()) {
        messageRequest.conversation_id = parseInt(targetConversationId);
      }

      console.log('发送API请求:', messageRequest);
      const aiResponse = await aiAPI.sendMessage(messageRequest);
      console.log('收到AI回复:', aiResponse);

      // 添加AI回复消息
      const aiMessage: Message = {
        id: aiResponse.id.toString(),
        content: aiResponse.content,
        sender: 'ai',
        timestamp: new Date(aiResponse.created_at),
        type: aiResponse.message_type as any
      };
      addMessage(aiMessage);

      // 如果是新对话，更新对话ID并重新加载对话列表
      if (aiResponse.conversation_id.toString() !== currentConversationId) {
        console.log('更新对话ID:', aiResponse.conversation_id);
        setCurrentConversationId(aiResponse.conversation_id.toString());
        // 重新加载对话列表
        await loadConversations();
      }

    } catch (error) {
      console.error('发送消息失败:', error);

      // 检查是否是认证错误
      if (error.message && error.message.includes('401')) {
        console.error('认证失败，可能需要重新登录');
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: '认证已过期，请重新登录后再试。',
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        };
        addMessage(errorMessage);
      } else {
        // 添加通用错误消息
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: '抱歉，发送消息失败，请稍后重试。',
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        };
        addMessage(errorMessage);
      }
    } finally {
      setIsTyping(false);
    }
  };

  // 在组件挂载时加载对话
  useEffect(() => {
    loadConversations();
  }, []);

  const value: AIContextType = {
    conversations,
    currentConversationId,
    currentMessages,
    isTyping,
    setConversations,
    setCurrentConversationId,
    setCurrentMessages,
    setIsTyping,
    addMessage,
    createNewConversation,
    switchConversation,
    deleteConversation,
    updateConversationTitle,
    sendMessageToAPI,
    loadConversations,
  };

  return <AIContext.Provider value={value}>{children}</AIContext.Provider>;
};
