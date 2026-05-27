# auto_label.py
import sqlite3
import pandas as pd
from datetime import datetime

def auto_label_all():
    conn = sqlite3.connect('learning_data.db')
    
    # 获取所有未标注的数据
    df = pd.read_sql("SELECT id, timestamp, window_title FROM sessions WHERE efficiency IS NULL", conn)
    
    if len(df) == 0:
        print("✅ 所有数据都已标注！")
        conn.close()
        return
    
    print(f"📊 开始自动标注 {len(df)} 条未标注数据...")
    
    updated = 0
    rules_applied = {
        'coding_high': 0,
        'late_night_low': 0,
        'document_medium': 0,
        'distraction_low': 0
    }
    
    for idx, row in df.iterrows():
        window = row['window_title'].lower()
        timestamp = pd.to_datetime(row['timestamp'])
        hour = timestamp.hour
        efficiency = None
        
        # 规则1：写代码 → 高效（5分）
        if any(app in window for app in ['visual studio code', 'pycharm', 'vscode', 'cursor', 'code']):
            efficiency = 5
            rules_applied['coding_high'] += 1
        
        # 规则2：深夜（23点后）刷视频/娱乐 → 低效（1分）
        elif hour >= 23 and any(app in window for app in ['youtube', 'bilibili', 'tiktok', 'netflix', '游戏']):
            efficiency = 1
            rules_applied['late_night_low'] += 1
        
        # 规则3：看文档/学习 → 中等高效（4分）
        elif any(app in window for app in ['pdf', 'word', 'notion', 'obsidian', '阅读', '文档']):
            efficiency = 4
            rules_applied['document_medium'] += 1
        
        # 规则4：工作时间（9-17点）刷娱乐 → 低效（2分）
        elif 9 <= hour <= 17 and any(app in window for app in ['youtube', 'bilibili', '微博', '小红书']):
            efficiency = 2
            rules_applied['distraction_low'] += 1
        
        # 其他情况保持 None，等待人工标注
        
        if efficiency is not None:
            c = conn.cursor()
            c.execute("UPDATE sessions SET efficiency = ? WHERE id = ?", (efficiency, row['id']))
            updated += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ 自动标注完成！")
    print(f"   共标注 {updated} 条数据")
    print(f"\n📋 规则命中统计：")
    print(f"   - 写代码（5分）: {rules_applied['coding_high']} 条")
    print(f"   - 深夜娱乐（1分）: {rules_applied['late_night_low']} 条")
    print(f"   - 看文档（4分）: {rules_applied['document_medium']} 条")
    print(f"   - 工作时间刷娱乐（2分）: {rules_applied['distraction_low']} 条")
    print(f"\n⚠️ 剩余 {len(df) - updated} 条需要人工标注")

if __name__ == "__main__":
    auto_label_all()