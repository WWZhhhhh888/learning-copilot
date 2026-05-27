# planner.py
import sqlite3
import pandas as pd
import joblib
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI
from feishu_bot import send_learning_plan

# 加载API Key
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    print("❌ 未找到API Key，请确保.env文件中有DEEPSEEK_API_KEY")
    exit()

# 初始化OpenAI客户端（用于DeepSeek）
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

print("🤖 加载AI模型...")

# 加载模型和应用编码
try:
    model = joblib.load('efficiency_model.pkl')
    app_codes = joblib.load('app_codes.pkl')
    print("✅ 模型加载成功")
except:
    print("❌ 模型文件未找到，请先运行 train_model.py")
    exit()

def predict_efficiency(hour, dayofweek, minute, app_name):
    """预测某个时间做某事的效率"""
    # 获取应用编码，如果未知则用默认值0
    app_code = app_codes.get(app_name, 0)
    
    features = pd.DataFrame([[hour, dayofweek, minute, app_code]], 
                           columns=['hour', 'dayofweek', 'minute', 'app_code'])
    pred = model.predict(features)[0]
    return round(pred, 1)

def get_tomorrow_schedule():
    """获取明天的效率预测"""
    tomorrow = datetime.now() + timedelta(days=1)
    dayofweek = tomorrow.weekday()
    
    schedule = []
    common_apps = list(app_codes.keys())[:5]  # 取最常见的5个应用
    
    for hour in range(8, 23):  # 8点到22点
        # 预测该时段的平均效率
        app = common_apps[0] if common_apps else "学习"
        efficiency = predict_efficiency(hour, dayofweek, 0, app)
        schedule.append({
            'hour': hour,
            'efficiency': efficiency,
            'time_range': f"{hour:02d}:00-{hour+1:02d}:00"
        })
    
    return schedule, dayofweek, tomorrow

def generate_plan_with_llm(schedule, dayofweek, date):
    """调用DeepSeek生成学习计划"""
    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    day_name = days[dayofweek]
    
    # 找出高效时段
    high_efficiency = [s for s in schedule if s['efficiency'] >= 4]
    low_efficiency = [s for s in schedule if s['efficiency'] <= 2.5]
    
    high_hours = ", ".join([str(s['hour']) for s in high_efficiency[:3]])
    low_hours = ", ".join([str(s['hour']) for s in low_efficiency[:3]])
    
    prompt = f"""
你是我的学习规划助手。

根据我对过去学习数据的分析，{date.strftime('%Y-%m-%d')}（{day_name}）的预测如下：

- 最高效时段：{high_hours}点（效率评分4-5分）
- 最低效时段：{low_hours}点（效率评分2.5分以下）

请帮我制定明天的学习计划，要求：
1. 把最难、最重要的任务安排在最高效的时段
2. 最低效时段安排轻松任务或休息
3. 输出格式：先是一段简短的文字建议，然后是一个JSON列表，每个任务包含：task（任务名）、time（时间段）、duration（时长，单位分钟）

示例输出格式：
根据你的数据，明天最清醒的时段是上午...建议如下：

[
  {{"task": "完成项目报告", "time": "09:00-11:00", "duration": 120}},
  {{"task": "复习英语单词", "time": "11:00-11:30", "duration": 30}}
]
"""
    
    print("📝 正在调用AI生成计划...")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        timeout=60
    )
    
    return response.choices[0].message.content

def main():
    print("\n" + "="*50)
    print("🎯 学习行为CoPilot - AI计划生成器")
    print("="*50 + "\n")
    
    # 获取预测
    schedule, dayofweek, tomorrow = get_tomorrow_schedule()
    
    # 显示预测概览
    print("📊 明天效率预测：")
    print("-" * 40)
    for s in schedule:
        emoji = "🔥" if s['efficiency'] >= 4 else "😴" if s['efficiency'] <= 2.5 else "👍"
        print(f"  {s['time_range']}: {s['efficiency']}分 {emoji}")
    print("-" * 40)
    
    # 生成AI计划
    print("\n🤖 正在生成个性化学习计划...\n")
    plan = generate_plan_with_llm(schedule, dayofweek, tomorrow)
    
    print("\n" + "="*50)
    print("📋 你的明日学习计划")
    print("="*50)
    print(plan)
    print("\n" + "="*50)
    
    # 保存计划到文件
    with open(f"plan_{tomorrow.strftime('%Y%m%d')}.md", "w") as f:
        f.write(f"# {tomorrow.strftime('%Y-%m-%d')} 学习计划\n\n")
        f.write(plan)
    print(f"\n💾 计划已保存到 plan_{tomorrow.strftime('%Y%m%d')}.md")
    
    # ===== 新增：推送到飞书 =====
    print("\n📤 正在推送到飞书...")
    success = send_learning_plan(plan)
    if success:
        print("✅ 计划已推送到飞书")
    else:
        print("❌ 飞书推送失败，请检查配置")

if __name__ == "__main__":
    main()