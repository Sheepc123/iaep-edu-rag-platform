import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  MessageCircle,
  Send,
  Search,
  Phone,
  Video,
  MoreVertical,
  Paperclip,
  Smile,
  User,
  Clock,
  CheckCheck,
  Circle,
  GraduationCap,
  Users
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import StudentLayout from "@/components/layouts/StudentLayout";

interface ChatMessage {
  id: string;
  content: string;
  sender: 'student' | 'teacher' | 'peer';
  senderName: string;
  timestamp: Date;
  status: 'sent' | 'delivered' | 'read';
  type: 'text' | 'image' | 'file';
}

interface Contact {
  id: string;
  name: string;
  role: 'teacher' | 'student';
  subject?: string;
  avatar: string;
  status: 'online' | 'offline' | 'busy';
  lastSeen?: Date;
  unreadCount: number;
}

export const ChatRoom = () => {
  // 模拟联系人数据
  const [contacts] = useState<Contact[]>([
    {
      id: '1',
      name: '李教授',
      role: 'teacher',
      subject: '高等数学',
      avatar: 'https://i.pravatar.cc/40?img=1',
      status: 'online',
      unreadCount: 2
    },
    {
      id: '2',
      name: '王老师',
      role: 'teacher',
      subject: '线性代数',
      avatar: 'https://i.pravatar.cc/40?img=2',
      status: 'offline',
      lastSeen: new Date(Date.now() - 3600000),
      unreadCount: 0
    },
    {
      id: '3',
      name: '张同学',
      role: 'student',
      avatar: 'https://i.pravatar.cc/40?img=3',
      status: 'online',
      unreadCount: 1
    },
    {
      id: '4',
      name: '刘同学',
      role: 'student',
      avatar: 'https://i.pravatar.cc/40?img=4',
      status: 'busy',
      unreadCount: 0
    }
  ]);

  const [selectedContact, setSelectedContact] = useState<Contact | null>(contacts[0]);

  // 为每个联系人模拟不同的聊天记录
  const getMessagesForContact = (contactId: string): ChatMessage[] => {
    const messageMap: Record<string, ChatMessage[]> = {
      '1': [ // 李教授
        {
          id: '1',
          content: '同学你好！有什么数学问题需要帮助吗？',
          sender: 'teacher',
          senderName: '李教授',
          timestamp: new Date(Date.now() - 3600000),
          status: 'read',
          type: 'text'
        },
        {
          id: '2',
          content: '老师好！我想请教一下关于极限的问题',
          sender: 'student',
          senderName: '我',
          timestamp: new Date(Date.now() - 3000000),
          status: 'read',
          type: 'text'
        }
      ],
      '2': [ // 王老师
        {
          id: '3',
          content: '线性代数有什么不懂的地方吗？',
          sender: 'teacher',
          senderName: '王老师',
          timestamp: new Date(Date.now() - 7200000),
          status: 'read',
          type: 'text'
        }
      ],
      '3': [ // 张同学
        {
          id: '4',
          content: '你好！我们一起学习吧',
          sender: 'peer',
          senderName: '张同学',
          timestamp: new Date(Date.now() - 1800000),
          status: 'read',
          type: 'text'
        },
        {
          id: '5',
          content: '好的！有什么问题可以互相讨论',
          sender: 'student',
          senderName: '我',
          timestamp: new Date(Date.now() - 1200000),
          status: 'read',
          type: 'text'
        }
      ],
      '4': [ // 刘同学
        {
          id: '6',
          content: '今天的作业你做完了吗？',
          sender: 'peer',
          senderName: '刘同学',
          timestamp: new Date(Date.now() - 900000),
          status: 'read',
          type: 'text'
        }
      ]
    };
    return messageMap[contactId] || [];
  };

  const [messages, setMessages] = useState<ChatMessage[]>(getMessagesForContact('1'));

  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState<'all' | 'teachers' | 'students'>('all');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 自动滚动到最新消息
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 切换联系人时更新消息
  useEffect(() => {
    if (selectedContact) {
      setMessages(getMessagesForContact(selectedContact.id));
    }
  }, [selectedContact]);

  // 发送消息
  const handleSendMessage = () => {
    if (!inputValue.trim() || !selectedContact) return;

    const newMessage: ChatMessage = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'student',
      senderName: '我',
      timestamp: new Date(),
      status: 'sent',
      type: 'text'
    };

    setMessages(prev => [...prev, newMessage]);
    setInputValue('');

    // 模拟回复
    setTimeout(() => {
      setIsTyping(true);
      setTimeout(() => {
        const reply: ChatMessage = {
          id: (Date.now() + 1).toString(),
          content: generateReply(inputValue, selectedContact.role),
          sender: selectedContact.role === 'teacher' ? 'teacher' : 'peer',
          senderName: selectedContact.name,
          timestamp: new Date(),
          status: 'delivered',
          type: 'text'
        };
        setMessages(prev => [...prev, reply]);
        setIsTyping(false);
      }, 2000);
    }, 500);
  };

  // 生成回复
  const generateReply = (studentMessage: string, role: 'teacher' | 'student'): string => {
    const lowerMessage = studentMessage.toLowerCase();
    
    if (role === 'teacher') {
      if (lowerMessage.includes('极限')) {
        return '关于极限问题，我们需要先理解极限的定义。你可以具体说说是哪个函数的极限吗？';
      }
      if (lowerMessage.includes('导数')) {
        return '导数是微积分的核心概念。你是想了解导数的定义，还是求导的方法？';
      }
      const teacherReplies = [
        '这是一个很好的问题！让我来为你详细解答。',
        '我理解你的困惑，这个知识点确实需要仔细理解。',
        '很高兴你能主动提问！学习就是要多思考多提问。'
      ];
      return teacherReplies[Math.floor(Math.random() * teacherReplies.length)];
    } else {
      const studentReplies = [
        '我也遇到过类似的问题，我们可以一起讨论一下！',
        '这个问题我之前也问过老师，可以分享一下经验。',
        '我们可以组队学习，互相帮助！'
      ];
      return studentReplies[Math.floor(Math.random() * studentReplies.length)];
    }
  };

  // 过滤联系人列表
  const filteredContacts = contacts.filter(contact => {
    const matchesSearch = contact.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         (contact.subject && contact.subject.toLowerCase().includes(searchQuery.toLowerCase()));
    
    if (activeTab === 'teachers') return contact.role === 'teacher' && matchesSearch;
    if (activeTab === 'students') return contact.role === 'student' && matchesSearch;
    return matchesSearch;
  });

  // 获取状态图标
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'online':
        return <div className="w-3 h-3 bg-green-500 rounded-full" />;
      case 'busy':
        return <div className="w-3 h-3 bg-yellow-500 rounded-full" />;
      default:
        return <div className="w-3 h-3 bg-gray-400 rounded-full" />;
    }
  };

  // 获取消息状态图标
  const getMessageStatusIcon = (status: string) => {
    switch (status) {
      case 'sent':
        return <Circle className="w-3 h-3 text-gray-400" />;
      case 'delivered':
        return <CheckCheck className="w-3 h-3 text-gray-400" />;
      case 'read':
        return <CheckCheck className="w-3 h-3 text-blue-500" />;
      default:
        return null;
    }
  };

  return (
    <StudentLayout>
      <div className="h-[calc(100vh-8rem)] flex bg-white rounded-2xl shadow-lg overflow-hidden">
        {/* 左侧联系人列表 */}
        <div className="w-80 bg-gray-50 border-r border-gray-200 flex flex-col">
          {/* 标题和标签页 */}
          <div className="p-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900 mb-3">聊天室</h2>
            <div className="flex space-x-1 bg-gray-100 rounded-lg p-1">
              {[
                { key: 'all', label: '全部' },
                { key: 'teachers', label: '老师' },
                { key: 'students', label: '同学' }
              ].map((tab) => (
                <button
                  key={tab.key}
                  onClick={() => setActiveTab(tab.key as any)}
                  className={`flex-1 px-3 py-1.5 text-sm rounded-md transition-colors ${
                    activeTab === tab.key
                      ? 'bg-white text-blue-600 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {/* 搜索栏 */}
          <div className="p-4 border-b border-gray-200">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="搜索联系人..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* 联系人列表 */}
          <div className="flex-1 overflow-y-auto">
            <div className="p-2 space-y-1">
              {filteredContacts.map((contact) => (
                <motion.div
                  key={contact.id}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => setSelectedContact(contact)}
                  className={`p-3 rounded-lg cursor-pointer transition-all duration-200 ${
                    selectedContact?.id === contact.id
                      ? 'bg-blue-100 border border-blue-200'
                      : 'bg-white hover:bg-gray-100 border border-gray-100'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <div className="relative">
                      <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                        contact.role === 'teacher' 
                          ? 'bg-gradient-to-r from-blue-500 to-purple-600' 
                          : 'bg-gradient-to-r from-green-500 to-teal-600'
                      }`}>
                        {contact.role === 'teacher' ? (
                          <GraduationCap className="w-6 h-6 text-white" />
                        ) : (
                          <User className="w-6 h-6 text-white" />
                        )}
                      </div>
                      <div className="absolute -bottom-1 -right-1">
                        {getStatusIcon(contact.status)}
                      </div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <h4 className="text-sm font-semibold text-gray-900 truncate">
                          {contact.name}
                        </h4>
                        {contact.unreadCount > 0 && (
                          <Badge className="bg-red-500 text-white text-xs px-1.5 py-0.5 min-w-[20px] h-5 flex items-center justify-center">
                            {contact.unreadCount}
                          </Badge>
                        )}
                      </div>
                      <p className="text-xs text-gray-600 truncate">
                        {contact.role === 'teacher' ? contact.subject : '同学'}
                      </p>
                      <div className="flex items-center mt-1">
                        <div className="flex items-center space-x-1 text-xs text-gray-500">
                          {contact.status === 'online' && (
                            <>
                              <Circle className="w-2 h-2 fill-green-500 text-green-500" />
                              <span>在线</span>
                            </>
                          )}
                          {contact.status === 'busy' && (
                            <>
                              <Circle className="w-2 h-2 fill-yellow-500 text-yellow-500" />
                              <span>忙碌</span>
                            </>
                          )}
                          {contact.status === 'offline' && contact.lastSeen && (
                            <>
                              <Clock className="w-2 h-2" />
                              <span>{contact.lastSeen.toLocaleTimeString()}</span>
                            </>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>

        {/* 右侧聊天界面 */}
        <div className="flex-1 flex flex-col">
          {selectedContact ? (
            <>
              {/* 聊天头部 */}
              <div className="flex items-center justify-between p-4 bg-white border-b border-gray-200">
                <div className="flex items-center space-x-3">
                  <div className="relative">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                      selectedContact.role === 'teacher'
                        ? 'bg-gradient-to-r from-blue-500 to-purple-600'
                        : 'bg-gradient-to-r from-green-500 to-teal-600'
                    }`}>
                      {selectedContact.role === 'teacher' ? (
                        <GraduationCap className="w-5 h-5 text-white" />
                      ) : (
                        <User className="w-5 h-5 text-white" />
                      )}
                    </div>
                    <div className="absolute -bottom-1 -right-1">
                      {getStatusIcon(selectedContact.status)}
                    </div>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">{selectedContact.name}</h3>
                    <p className="text-sm text-gray-600">
                      {selectedContact.role === 'teacher' ? selectedContact.subject : '同学'}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Button variant="ghost" size="sm" className="p-2">
                    <Phone className="w-4 h-4" />
                  </Button>
                  <Button variant="ghost" size="sm" className="p-2">
                    <Video className="w-4 h-4" />
                  </Button>
                  <Button variant="ghost" size="sm" className="p-2">
                    <MoreVertical className="w-4 h-4" />
                  </Button>
                </div>
              </div>

              {/* 消息区域 */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gradient-to-b from-gray-50 to-white">
                {messages.map((message, index) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.1 }}
                    className={`flex ${message.sender === 'student' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`max-w-[70%] ${message.sender === 'student' ? 'order-2' : 'order-1'}`}>
                      <div
                        className={`relative p-3 rounded-2xl shadow-sm ${
                          message.sender === 'student'
                            ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white ml-4'
                            : message.sender === 'teacher'
                            ? 'bg-white text-gray-800 border border-gray-100 mr-4'
                            : 'bg-green-100 text-gray-800 border border-green-200 mr-4'
                        }`}
                      >
                        <div className="text-sm leading-relaxed">
                          {message.content}
                        </div>
                        <div className={`flex items-center justify-between mt-2 text-xs ${
                          message.sender === 'student' ? 'text-blue-100' : 'text-gray-500'
                        }`}>
                          <span>{message.timestamp.toLocaleTimeString()}</span>
                          {message.sender === 'student' && (
                            <div className="ml-2">
                              {getMessageStatusIcon(message.status)}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* 头像 */}
                    {message.sender !== 'student' ? (
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center mr-3 order-0 flex-shrink-0 ${
                        message.sender === 'teacher'
                          ? 'bg-gradient-to-r from-blue-500 to-purple-600'
                          : 'bg-gradient-to-r from-green-500 to-teal-600'
                      }`}>
                        {message.sender === 'teacher' ? (
                          <GraduationCap className="w-4 h-4 text-white" />
                        ) : (
                          <User className="w-4 h-4 text-white" />
                        )}
                      </div>
                    ) : (
                      <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center ml-3 order-3 flex-shrink-0">
                        <User className="w-4 h-4 text-gray-600" />
                      </div>
                    )}
                  </motion.div>
                ))}

                {/* 正在输入指示器 */}
                {isTyping && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex justify-start"
                  >
                    <div className="flex items-start space-x-3">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                        selectedContact.role === 'teacher'
                          ? 'bg-gradient-to-r from-blue-500 to-purple-600'
                          : 'bg-gradient-to-r from-green-500 to-teal-600'
                      }`}>
                        {selectedContact.role === 'teacher' ? (
                          <GraduationCap className="w-4 h-4 text-white" />
                        ) : (
                          <User className="w-4 h-4 text-white" />
                        )}
                      </div>
                      <div className="bg-white border border-gray-100 p-3 rounded-2xl shadow-sm">
                        <div className="flex space-x-1">
                          {[0, 1, 2].map((i) => (
                            <motion.div
                              key={i}
                              className="w-2 h-2 bg-gray-400 rounded-full"
                              animate={{ scale: [1, 1.3, 1], opacity: [0.5, 1, 0.5] }}
                              transition={{ duration: 0.8, repeat: Infinity, delay: i * 0.2 }}
                            />
                          ))}
                        </div>
                      </div>
                    </div>
                  </motion.div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* 输入区域 */}
              <div className="p-4 bg-white border-t border-gray-200">
                <div className="flex items-end space-x-3">
                  <Button variant="ghost" size="sm" className="p-2 text-gray-500">
                    <Paperclip className="w-4 h-4" />
                  </Button>
                  <div className="flex-1 relative">
                    <textarea
                      value={inputValue}
                      onChange={(e) => setInputValue(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                          e.preventDefault();
                          handleSendMessage();
                        }
                      }}
                      placeholder="输入消息... (Shift+Enter 换行)"
                      className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none min-h-[44px] max-h-32"
                      rows={1}
                    />
                  </div>
                  <Button variant="ghost" size="sm" className="p-2 text-gray-500">
                    <Smile className="w-4 h-4" />
                  </Button>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleSendMessage}
                    disabled={!inputValue.trim()}
                    className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-2xl flex items-center justify-center text-white transition-all duration-200 shadow-lg"
                  >
                    <Send className="w-4 h-4" />
                  </motion.button>
                </div>
              </div>
            </>
          ) : (
            /* 未选择联系人时的占位界面 */
            <div className="flex-1 flex items-center justify-center bg-gray-50">
              <div className="text-center">
                <div className="w-20 h-20 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
                  <MessageCircle className="w-10 h-10 text-gray-400" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">选择联系人开始聊天</h3>
                <p className="text-gray-600">从左侧列表中选择老师或同学，开始学习交流</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </StudentLayout>
  );
};
