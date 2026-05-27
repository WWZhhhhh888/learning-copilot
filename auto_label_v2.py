# auto_label_v2.py
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
        'chrome_learning': 0,
        'bilibili_low': 0,
        'wechat_work': 0,
        'xiaohongshu_low': 0,
        'safari_learning': 0,
        'unknown_medium': 0
    }
    
    for idx, row in df.iterrows():
        window = row['window_title'].lower()
        timestamp = pd.to_datetime(row['timestamp'])
        hour = timestamp.hour
        efficiency = None
        
        # 规则1：Chrome（学习时段 8-18点）→ 3分（默认）
        if 'google chrome' in window or 'chrome' in window:
            if 8 <= hour <= 18:
                efficiency = 3
                rules_applied['chrome_learning'] += 1
            else:
                efficiency = 2
                rules_applied['chrome_learning'] += 1
        
        # 规则2：哔哩哔哩（娱乐，低效）
        elif '哔哩哔哩' in window or 'bilibili' in window:
            if hour >= 22:
                efficiency = 1  # 深夜刷B站，很低效
            elif 9 <= hour <= 17:
                efficiency = 2  # 工作时间刷，低效
            else:
                efficiency = 2  # 其他时段
            rules_applied['bilibili_low'] += 1
        
        # 规则3：小红书（娱乐，低效）
        elif '小红书' in window:
            if 9 <= hour <= 17:
                efficiency = 2
            else:
                efficiency = 2
            rules_applied['xiaohongshu_low'] += 1
        
        # 规则4：微信（白天工作沟通 → 3分，晚上闲聊 → 2分）
        elif '微信' in window:
            if 9 <= hour <= 18:
                efficiency = 3
            else:
                efficiency = 2
            rules_applied['wechat_work'] += 1
        
        # 规则5：Safari（类似Chrome）
        elif 'safari' in window:
            if 8 <= hour <= 18:
                efficiency = 3
            else:
                efficiency = 2
            rules_applied['safari_learning'] += 1
        
        # 规则6：Unknown（无法判断 → 默认3分）
        elif 'unknown' in window:
            efficiency = 3
            rules_applied['unknown_medium'] += 1
        
        if efficiency is not None:
            c = conn.cursor()
            c.execute("UPDATE sessions SET efficiency = ? WHERE id = ?", (efficiency, row['id']))
            updated += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ 自动标注完成！")
    print(f"   共标注 {updated} 条数据")
    print(f"\n📋 规则命中统计：")
    print(f"   - Chrome: {rules_applied['chrome_learning']} 条")
    print(f"   - 哔哩哔哩: {rules_applied['bilibili_low']} 条")
    print(f"   - 小红书: {rules_applied['xiaohongshu_low']} 条")
    print(f"   - 微信: {rules_applied['wechat_work']} 条")
    print(f"   - Safari: {rules_applied['safari_learning']} 条")
    print(f"   - Unknown: {rules_applied['unknown_medium']} 条")
    print(f"\n⚠️ 剩余 {len(df) - updated} 条需要人工标注")

if __name__ == "__main__":
    auto_label_all()