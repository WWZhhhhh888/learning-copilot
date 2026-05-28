import re

# 存储凑单会话
sessions = {}

def handle_group_buy(message, user, group_id):
    """
    处理凑单相关消息
    返回：机器人回复内容，如果不需要回复则返回 None
    """
    # 1. 发起凑单：我要凑单，目标50元
    if "我要凑单" in message:
        target = extract_amount(message)
        sessions[group_id] = {
            "target": target,
            "current": 0,
            "orders": [],
            "initiator": user,
            "status": "active"
        }
        return f"""✅ 发起凑单！
目标：{target}元
当前：0元
状态：进行中

💡 回复「+商品名，价格」加单
💡 回复「凑单状态」查看当前订单"""

    # 2. 加单：+汉堡，15元
    match = re.search(r'\+(\S+)[，,]\s*(\d+(\.\d+)?)元?', message)
    if match:
        item = match.group(1)
        price = float(match.group(2))
        
        session = sessions.get(group_id)
        if not session or session.get("status") != "active":
            return None
        
        session["current"] += price
        session["orders"].append({
            "user": user,
            "item": item,
            "price": price
        })
        
        reply = f"✅ {user} 加了 {item}({price}元)\n"
        reply += f"当前：{session['current']}/{session['target']}元\n"
        
        if session["current"] >= session["target"]:
            per_person = session["current"] / len(session["orders"])
            reply += f"\n🎉 凑单成功！\n总额：{session['current']}元\n人数：{len(session['orders'])}人\n人均：{per_person:.1f}元"
            session["status"] = "completed"
        
        return reply

    # 3. 查看状态
    if "凑单状态" in message:
        session = sessions.get(group_id)
        if not session or session.get("status") != "active":
            return None
        
        reply = f"📊 当前凑单状态：\n"
        reply += f"目标：{session['target']}元\n"
        reply += f"当前：{session['current']}元\n"
        reply += f"差额：{session['target'] - session['current']}元\n"
        if session["orders"]:
            reply += f"\n📋 订单明细：\n"
            for o in session["orders"][-5:]:
                reply += f"{o['user']}：{o['item']}({o['price']}元)\n"
        return reply

    return None

def extract_amount(text):
    match = re.search(r'(\d+(\.\d+)?)元', text)
    if match:
        return float(match.group(1))
    return 50

if __name__ == "__main__":
    test_group = "test_group_001"
    print("=== 测试凑单机器人 ===\n")
    
    msg = "我要凑单，目标50元"
    reply = handle_group_buy(msg, "用户A", test_group)
    print(f"用户A: {msg}")
    print(f"机器人: {reply}\n")
    
    msg = "+汉堡，15元"
    reply = handle_group_buy(msg, "用户A", test_group)
    print(f"用户A: {msg}")
    print(f"机器人: {reply}\n")
    
    msg = "+薯条，12元"
    reply = handle_group_buy(msg, "用户B", test_group)
    print(f"用户B: {msg}")
    print(f"机器人: {reply}\n")
    
    msg = "+鸡块，23元"
    reply = handle_group_buy(msg, "用户C", test_group)
    print(f"用户C: {msg}")
    print(f"机器人: {reply}\n")
