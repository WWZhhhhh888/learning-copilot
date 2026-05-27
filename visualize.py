# visualize.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 连接数据库
conn = sqlite3.connect('learning_data.db')
df = pd.read_sql("SELECT timestamp, window_title, efficiency FROM sessions WHERE efficiency IS NOT NULL", conn)
conn.close()

# 转换时间
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour
df['dayofweek'] = df['timestamp'].dt.dayofweek
df['date'] = df['timestamp'].dt.date

# 提取应用名
df['app'] = df['window_title'].apply(lambda x: str(x).split(':')[0] if ':' in str(x) else str(x))

print(f"📊 共 {len(df)} 条标注数据")
print("="*50)

# 1. 各时段平均效率
print("\n1️⃣ 各时段平均效率（小时）")
hourly_eff = df.groupby('hour')['efficiency'].mean().sort_index()
print(hourly_eff)

plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
hourly_eff.plot(kind='bar', color='steelblue')
plt.title('各时段平均效率')
plt.xlabel('小时')
plt.ylabel('平均效率 (1-5分)')
plt.xticks(rotation=0)

# 2. 各应用平均效率（Top 15）
print("\n2️⃣ 各应用平均效率（Top 15）")
app_eff = df.groupby('app')['efficiency'].agg(['mean', 'count']).sort_values('mean', ascending=False).head(15)
print(app_eff)

plt.subplot(2, 2, 2)
colors = ['green' if x >= 4 else 'orange' if x >= 3 else 'red' for x in app_eff['mean']]
app_eff['mean'].plot(kind='barh', color=colors)
plt.title('各应用平均效率')
plt.xlabel('平均效率')
plt.gca().invert_yaxis()

# 3. 效率分布直方图
plt.subplot(2, 2, 3)
df['efficiency'].hist(bins=5, color='purple', edgecolor='black')
plt.title('效率分布直方图')
plt.xlabel('效率评分')
plt.ylabel('频次')

# 4. 星期几 vs 小时 热力图
pivot_table = df.pivot_table(index='dayofweek', columns='hour', values='efficiency', aggfunc='mean')
days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
plt.subplot(2, 2, 4)
sns.heatmap(pivot_table, cmap='YlOrRd', annot=False, cbar_kws={'label': '平均效率'})
plt.title('星期-小时 效率热力图')
plt.xlabel('小时')
plt.ylabel('星期')
plt.yticks(ticks=range(7), labels=days)

plt.tight_layout()
plt.savefig('data_visualization.png', dpi=150, bbox_inches='tight')
print("\n✅ 图表已保存为 data_visualization.png")

# 5. 额外：数据量增长趋势
plt.figure(figsize=(12, 5))
daily_counts = df.groupby('date').size().sort_index()
plt.plot(daily_counts.index, daily_counts.values, marker='o', linestyle='-', color='teal')
plt.title('数据量增长趋势')
plt.xlabel('日期')
plt.ylabel('当日标注数量')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('data_growth.png', dpi=150, bbox_inches='tight')
print("✅ 增长趋势图已保存为 data_growth.png")

print("\n🎉 可视化完成！")