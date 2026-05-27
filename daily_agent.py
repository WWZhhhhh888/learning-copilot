# daily_agent.py
import schedule
import time
from datetime import datetime
from planner import main as generate_plan

def morning_job():
    print(f"\n[{datetime.now()}] 🚀 开始执行每日学习计划推送...")
    print("-" * 40)
    generate_plan()
    print("-" * 40)
    print(f"[{datetime.now()}] ✅ 执行完成\n")

# 每天早上8点执行
schedule.every().day.at("08:00").do(morning_job)

print("=" * 50)
print("🤖 学习Agent已启动")
print("=" * 50)
print("📅 定时任务：每天早上 08:00 自动推送学习计划")
print("⏸️  按 Ctrl+C 停止运行\n")

while True:
    schedule.run_pending()
    time.sleep(60)