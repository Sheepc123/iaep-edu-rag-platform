import StudentLayout from "@/components/layouts/StudentLayout";
import { AbilityRadarChart } from "@/components/charts/AbilityRadarChart";
import { CheckSquare, BookOpen, Clock, Zap, Lightbulb } from "lucide-react";

// Main Dashboard Component
export const Dashboard = () => {
  return (
    <StudentLayout>
      <div className="grid grid-cols-2 gap-8">
        {/* Row 1 */}
        <WelcomeCard />
        <KeyMetrics />

        {/* Row 2 */}
        <TodoListCard />
        <CoursesCard />

        {/* Row 3 (Full Width) */}
        <div className="col-span-2">
          <AbilityCard />
        </div>
      </div>
    </StudentLayout>
  );
};

// Card component
const Card = ({ children, className = "" }: { children: React.ReactNode, className?: string }) => (
  <div className={`bg-white/60 backdrop-blur-xl p-6 rounded-lg border border-white/20 shadow-sm h-full transition-all duration-300 ease-in-out hover:scale-[1.02] hover:shadow-lg hover:shadow-blue-500/10 cursor-pointer ${className}`}>
    {children}
  </div>
);

// Welcome & AI Suggestion Card
const WelcomeCard = () => (
  <Card className="flex flex-col justify-center">
    <h2 className="text-3xl font-bold text-gray-800">你好, [学生姓名]!</h2>
    <div className="mt-4 flex items-center p-4 bg-white rounded-lg border-l-4 border-brand">
        <Lightbulb className="text-brand mr-4" size={24} />
        <div>
            <h3 className="font-semibold text-gray-700">AI 学习建议</h3>
            <p className="text-gray-500">根据你最近的练习记录，建议加强 "函数与极限" 章节的学习。</p>
        </div>
    </div>
  </Card>
);

// Key Metrics Card
const KeyMetrics = () => (
  <Card>
    <div className="flex justify-around items-center h-full">
      <MetricItem value="75" unit="分钟" label="今日学习" />
      <MetricItem value="3" unit="个" label="待办完成" />
      <MetricItem value="85" unit="分" label="平均得分" />
    </div>
  </Card>
);

const MetricItem = ({ value, unit, label }: { value: string, unit: string, label: string }) => (
  <div className="text-center">
    <p className="text-4xl font-bold text-brand">{value}<span className="text-lg ml-1 text-gray-500">{unit}</span></p>
    <p className="text-gray-500 mt-1">{label}</p>
  </div>
);

// To-Do List Card
const TodoListCard = () => (
  <Card>
    <h3 className="font-bold text-xl text-gray-800 mb-4">待办事项</h3>
    <ul className="space-y-3">
      <TodoItem label="完成第三章的在线测试" isDone />
      <TodoItem label={'观看 "导数应用" 视频'} isDone={false} />
      <TodoItem label={'阅读 "积分方法" 补充材料'} isDone={false} />
    </ul>
  </Card>
);

const TodoItem = ({ label, isDone }: { label: string, isDone: boolean }) => (
  <li className="flex items-center">
    <CheckSquare className={`mr-3 ${isDone ? "text-brand" : "text-gray-300"}`} />
    <span className={`${isDone ? "line-through text-gray-400" : "text-gray-700"}`}>{label}</span>
  </li>
);

// My Courses Card
const CoursesCard = () => (
  <Card>
    <h3 className="font-bold text-xl text-gray-800 mb-4">我的课程</h3>
    <div className="space-y-4">
        <CourseItem title="高等数学 (上)" progress={75} />
        <CourseItem title="线性代数" progress={40} />
    </div>
  </Card>
);

const CourseItem = ({ title, progress }: { title: string, progress: number }) => (
    <div>
        <div className="flex justify-between items-center mb-1">
            <p className="font-semibold text-gray-700">{title}</p>
            <p className="text-sm text-gray-500">{progress}%</p>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-brand h-2 rounded-full" style={{ width: `${progress}%` }}></div>
        </div>
    </div>
);


// Ability Model Card
const AbilityCard = () => (
  <Card>
    <h3 className="font-bold text-xl text-gray-800 mb-2">综合能力评估</h3>
    <div className="h-80">
        <AbilityRadarChart />
    </div>
  </Card>
);
