from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import requests
from datetime import datetime

app = FastAPI()

class Todo(BaseModel):
    task: str
    time: str
    priority: str = "medium"

# 飞书webhook（替换成你自己的）
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/你的hook"

def send_feishu(msg):
    requests.post(FEISHU_WEBHOOK, json={"msg_type": "text", "content": {"text": msg}})

@app.post("/todo")
def create_todo(todo: Todo):
    # 存数据库
    conn = sqlite3.connect("todos.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, task TEXT, time TEXT, status TEXT)")
    c.execute("INSERT INTO todos (task, time, status) VALUES (?, ?, ?)", (todo.task, todo.time, "pending"))
    conn.commit()
    conn.close()
    
    # 发飞书提醒
    send_feishu(f"⏰ 待办提醒\n任务：{todo.task}\n时间：{todo.time}")
    
    return {"status": "ok", "task": todo.task}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
