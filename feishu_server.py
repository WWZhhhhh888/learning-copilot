from flask import Flask, request, jsonify
from group_buy import handle_group_buy
import json

app = Flask(__name__)

VERIFICATION_TOKEN = "hxhaEv07xDSUvcLAJrhPmgvMAUi3nYmG"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})
    
    if data.get("type") == "event_callback":
        event = data.get("event", {})
        if event.get("type") == "im.message.receive_v1":
            message = event.get("message", {})
            content = json.loads(message.get("content", "{}"))
            user_message = content.get("text", "")
            user = event.get("sender", {}).get("sender_id", {}).get("user_id", "unknown")
            group_id = message.get("chat_id", "unknown")
            
            reply = handle_group_buy(user_message, user, group_id)
            
            if reply:
                from feishu_bot import send_feishu_message
                send_feishu_message(reply)
    
    return jsonify({"code": 0})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
