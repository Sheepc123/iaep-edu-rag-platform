import React, { createContext, useContext, useState, ReactNode } from 'react';

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
  switchConversation: (conversationId: string) => void;
  deleteConversation: (conversationId: string) => void;
  updateConversationTitle: (conversationId: string, title: string) => void;
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
  const [conversations, setConversations] = useState<Conversation[]>([
    {
      id: '1',
      title: '欢迎使用AI助手',
      messages: [
        {
          id: '1',
          content: '你好！我是你的AI学习助手小智，我可以帮助你：\n\n📚 解答学习问题\n🎯 制定学习计划\n📊 分析学习进度\n💡 提供学习建议\n\n有什么可以帮助你的吗？',
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        }
      ],
      lastUpdated: new Date()
    }
  ]);

  const [currentConversationId, setCurrentConversationId] = useState<string>('1');
  const [currentMessages, setCurrentMessages] = useState<Message[]>(conversations[0].messages);
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

  const switchConversation = (conversationId: string) => {
    const conversation = conversations.find(c => c.id === conversationId);
    if (conversation) {
      setCurrentConversationId(conversationId);
      setCurrentMessages(conversation.messages);
    }
  };

  const deleteConversation = (conversationId: string) => {
    if (conversations.length <= 1) return; // 至少保留一个对话
    
    const updatedConversations = conversations.filter(c => c.id !== conversationId);
    setConversations(updatedConversations);
    
    if (currentConversationId === conversationId) {
      const firstConversation = updatedConversations[0];
      setCurrentConversationId(firstConversation.id);
      setCurrentMessages(firstConversation.messages);
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
  };

  return <AIContext.Provider value={value}>{children}</AIContext.Provider>;
};
