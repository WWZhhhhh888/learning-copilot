from group_buy import handle_group_buy

group_id = "cli_test"
print("凑单机器人 CLI 测试模式")
print("输入命令：")
print("  - 我要凑单，目标XX元")
print("  - +商品名，价格")
print("  - 凑单状态")
print("  - exit 退出")
print("-" * 40)

while True:
    user = input("\n用户: ")
    if user.lower() == "exit":
        break
    reply = handle_group_buy(user, "测试用户", group_id)
    if reply:
        print(f"机器人: {reply}")
    else:
        print("机器人: (无响应，请检查命令格式)")
