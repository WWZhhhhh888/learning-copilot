import json
import logging
from lark_oapi import Client, Request, Response
from lark_oapi import LOGGER
from lark_oapi.api.im.v1 import P2ImMessageReceiveV1

# 你的 App ID 和 App Secret
APP_ID = "cli_aa92f7120a381cb1"
APP_SECRET = "V5MS0HQwIa7YHY5uvm9ejgYg1F0UbNS3"

def on_p2_im_message_receive_v1(event: P2ImMessageReceiveV1) -> None:
    """处理接收到的消息"""
    message = event.event.message
    content = json.loads(message.content)
    user_message = content.get("text", "")
    user = message.sender_id.user_id if message.sender_id else "unknown"
    group_id = message.chat_id
    
    print(f"收到消息: {user_message} 来自 {user}")
    
    # 调用凑单机器人
    from group_buy import handle_group_buy
    reply = handle_group_buy(user_message, user, group_id)
    
    if reply:
        # 发送回复
        from feishu_bot import send_feishu_message
        send_feishu_message(reply)
        print(f"已回复: {reply[:50]}...")

def main():
    # 创建客户端
    client = Client.builder() \
        .app_id(APP_ID) \
        .app_secret(APP_SECRET) \
        .build()
    
    # 注册事件处理器
    client.events().register_p2_im_message_receive_v1(on_p2_im_message_receive_v1)
    
    print("=" * 50)
    print("长连接已启动，等待消息...")
    print("在飞书群里 @机器人 发送消息")
    print("按 Ctrl+C 停止")
    print("=" * 50)
    
    # 启动长连接
    client.events().start_loop()

if __name__ == "__main__":
    main()
