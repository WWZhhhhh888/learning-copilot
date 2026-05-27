# train_model.py
import sqlite3
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

print("📊 加载数据...")

# 连接数据库
conn = sqlite3.connect('learning_data.db')
df = pd.read_sql("SELECT timestamp, window_title, efficiency FROM sessions WHERE efficiency IS NOT NULL", conn)
conn.close()

# 转换时间戳
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour
df['dayofweek'] = df['timestamp'].dt.dayofweek
df['minute'] = df['timestamp'].dt.minute

# 提取应用名称（窗口标题的第一部分）
df['app_name'] = df['window_title'].apply(lambda x: str(x).split(':')[0] if ':' in str(x) else str(x))

# 创建应用名称的数值编码
app_codes = {app: i for i, app in enumerate(df['app_name'].unique())}
df['app_code'] = df['app_name'].map(app_codes)

print(f"✅ 加载完成，共 {len(df)} 条标注数据")
print(f"📱 共发现 {len(app_codes)} 个不同的应用/窗口")

# 准备特征和标签
features = ['hour', 'dayofweek', 'minute', 'app_code']
X = df[features]
y = df['efficiency']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练模型
print("🤖 训练随机森林模型...")
model = RandomForestRegressor(n_estimators=50, random_state=42)
model.fit(X_train, y_train)

# 评估模型
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"✅ 模型训练完成！")
print(f"📈 平均绝对误差: {mae:.2f} 分")

# 保存模型和应用编码
joblib.dump(model, 'efficiency_model.pkl')
joblib.dump(app_codes, 'app_codes.pkl')
print("💾 模型已保存为 efficiency_model.pkl")
print("💾 应用编码已保存为 app_codes.pkl")

# 显示特征重要性
feature_importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
print("\n📊 特征重要性:")
print(feature_importance)