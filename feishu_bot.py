import requests
import json
from datetime import datetime
from group_buy import handle_group_buy

# 你的 Webhook 地址
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/5976aa51-5081-440b-a289-0a297f58e3f6"

def send_feishu_message(content: str, msg_type: str = "text") -> bool:
    """发送消息到飞书群"""
    payload = {
        "msg_type": msg_type,
        "content": {
            "text": content
        }
    }
    
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            print(f"✅ 消息发送成功: {datetime.now()}")
            return True
        else:
            print(f"❌ 发送失败: {result.get('msg', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

def send_learning_plan(plan_text: str):
    """发送学习计划"""
    message = f"【学习计划】\n{plan_text}"
    return send_feishu_message(message)

def process_feishu_message(message: str, user: str, group_id: str):
    """处理飞书收到的消息"""
    reply = handle_group_buy(message, user, group_id)
    if reply:
        send_feishu_message(reply)
        return True
    return False

if __name__ == "__main__":
    test_msg = "测试消息：飞书机器人配置成功！"
    send_learning_plan(test_msg)
