import requests
import json

TODO_API = "http://localhost:8000/todo"

# 模拟计划中的任务
test_plan = '''
[
  {"task": "攻克高数核心难点", "time": "10:00-12:00", "duration": 120},
  {"task": "整理笔记", "time": "14:00-15:00", "duration": 60}
]
'''

def extract_tasks_from_plan(plan_text):
    tasks = []
    json_match = __import__('re').search(r'\[\s*\{.*?\}\s*\]', plan_text, __import__('re').DOTALL)
    if json_match:
        try:
            tasks_data = json.loads(json_match.group())
            for t in tasks_data:
                tasks.append({
                    "task": t.get("task", ""),
                    "time": t.get("time", ""),
                    "priority": "high" if "攻克" in t.get("task", "") else "medium"
                })
        except:
            pass
    return tasks

def sync_to_todo(tasks):
    for task in tasks:
        if task["task"] and task["time"]:
            resp = requests.post(TODO_API, json={
                "task": task["task"],
                "time": task["time"],
                "priority": task["priority"]
            })
            if resp.status_code == 200:
                print(f"✅ 已同步：{task['task']} @ {task['time']}")
            else:
                print(f"❌ 同步失败：{task['task']}")

print("测试待办同步...")
tasks = extract_tasks_from_plan(test_plan)
sync_to_todo(tasks)
print("测试完成")
