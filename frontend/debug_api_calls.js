// 前端API调用调试脚本
// 在浏览器控制台中运行此脚本来调试API问题

console.log('🔧 开始调试前端API调用...');

// 1. 测试基本API连接
async function testBasicConnection() {
  console.log('\n1. 测试基本连接...');
  
  try {
    const response = await fetch('http://localhost:8000/health');
    if (response.ok) {
      console.log('✅ 后端服务连接正常');
      return true;
    } else {
      console.log('❌ 后端服务响应异常:', response.status);
      return false;
    }
  } catch (error) {
    console.log('❌ 无法连接后端服务:', error);
    return false;
  }
}

// 2. 测试登录
async function testLogin() {
  console.log('\n2. 测试登录...');
  
  try {
    const response = await fetch('http://localhost:8000/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: 'teacher1',
        password: '123456',
        remember_me: false
      })
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ 登录成功');
      console.log('Token:', data.access_token.substring(0, 20) + '...');
      return data.access_token;
    } else {
      console.log('❌ 登录失败:', response.status);
      const errorText = await response.text();
      console.log('错误信息:', errorText);
      return null;
    }
  } catch (error) {
    console.log('❌ 登录异常:', error);
    return null;
  }
}

// 3. 测试课程练习API
async function testCourseExercisesAPI(token) {
  console.log('\n3. 测试课程练习API...');
  
  if (!token) {
    console.log('❌ 没有有效token');
    return false;
  }
  
  try {
    const response = await fetch('http://localhost:8000/api/v1/courses/1/exercises', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      }
    });
    
    console.log('响应状态:', response.status);
    console.log('响应头:', Object.fromEntries(response.headers.entries()));
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ API调用成功');
      console.log('响应数据:', data);
      
      const exercises = data.exercises || [];
      console.log(`获取到 ${exercises.length} 个练习:`);
      exercises.forEach((ex, index) => {
        console.log(`  ${index + 1}. ${ex.title} (${ex.category})`);
      });
      
      return true;
    } else {
      console.log('❌ API调用失败:', response.status);
      const errorText = await response.text();
      console.log('错误信息:', errorText);
      return false;
    }
  } catch (error) {
    console.log('❌ API调用异常:', error);
    return false;
  }
}

// 4. 测试CORS
async function testCORS() {
  console.log('\n4. 测试CORS...');
  
  try {
    const response = await fetch('http://localhost:8000/api/v1/courses/1/exercises', {
      method: 'OPTIONS'
    });
    
    console.log('OPTIONS响应状态:', response.status);
    console.log('CORS头信息:');
    
    const corsHeaders = [
      'access-control-allow-origin',
      'access-control-allow-methods',
      'access-control-allow-headers',
      'access-control-allow-credentials'
    ];
    
    corsHeaders.forEach(header => {
      const value = response.headers.get(header);
      console.log(`  ${header}: ${value || '未设置'}`);
    });
    
    return true;
  } catch (error) {
    console.log('❌ CORS测试失败:', error);
    return false;
  }
}

// 5. 模拟前端API调用
async function simulateFrontendCall() {
  console.log('\n5. 模拟前端API调用...');
  
  // 模拟前端的apiRequest函数
  async function apiRequest(endpoint, options = {}) {
    const baseURL = 'http://localhost:8000/api/v1';
    const url = `${baseURL}${endpoint}`;
    
    const defaultOptions = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    };
    
    const finalOptions = { ...defaultOptions, ...options };
    
    console.log('请求URL:', url);
    console.log('请求选项:', finalOptions);
    
    try {
      const response = await fetch(url, finalOptions);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API请求失败:', error);
      throw error;
    }
  }
  
  // 获取token
  const token = await testLogin();
  if (!token) return false;
  
  try {
    // 模拟getCourseExercises调用
    const result = await apiRequest('/courses/1/exercises', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      }
    });
    
    console.log('✅ 前端API调用模拟成功');
    console.log('返回数据:', result);
    return true;
  } catch (error) {
    console.log('❌ 前端API调用模拟失败:', error);
    return false;
  }
}

// 主测试函数
async function runAllTests() {
  console.log('🚀 开始完整API调试测试');
  console.log('=' * 50);
  
  let successCount = 0;
  
  if (await testBasicConnection()) successCount++;
  
  const token = await testLogin();
  if (token) successCount++;
  
  if (await testCourseExercisesAPI(token)) successCount++;
  if (await testCORS()) successCount++;
  if (await simulateFrontendCall()) successCount++;
  
  console.log('\n' + '='.repeat(50));
  console.log(`🎯 测试完成: ${successCount}/5 项通过`);
  
  if (successCount >= 4) {
    console.log('🎉 API调用基本正常！');
    console.log('\n💡 如果前端仍有问题，请检查:');
    console.log('1. 浏览器控制台的具体错误信息');
    console.log('2. 网络标签页中的请求详情');
    console.log('3. 前端代码中的错误处理');
  } else {
    console.log('❌ 仍有问题需要解决');
    console.log('\n🔧 建议:');
    console.log('1. 确保后端服务正在运行');
    console.log('2. 检查CORS配置');
    console.log('3. 验证数据库中有练习数据');
  }
}

// 运行测试
runAllTests().catch(console.error);

// 导出函数供手动调用
window.debugAPI = {
  testBasicConnection,
  testLogin,
  testCourseExercisesAPI,
  testCORS,
  simulateFrontendCall,
  runAllTests
};

console.log('\n💡 可以手动调用以下函数进行单独测试:');
console.log('- debugAPI.testBasicConnection()');
console.log('- debugAPI.testLogin()');
console.log('- debugAPI.testCourseExercisesAPI(token)');
console.log('- debugAPI.testCORS()');
console.log('- debugAPI.simulateFrontendCall()');
console.log('- debugAPI.runAllTests()');
