# app.py
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="学习行为CoPilot", layout="wide")

st.title("📚 学习行为CoPilot")
st.markdown("基于AI的个性化学习规划器")

# 侧边栏
with st.sidebar:
    st.header("⚙️ 设置")
    st.write("数据采集间隔: 60秒")
    st.write(f"最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 主区域 - 数据概览
st.header("📊 学习行为概览")

# 从数据库读取数据
conn = sqlite3.connect('learning_data.db')
df = pd.read_sql("SELECT timestamp, window_title, efficiency FROM sessions", conn)
conn.close()

if len(df) == 0:
    st.info("暂无数据。请先运行数据采集脚本：`python data_collector.py`")
    st.stop()

# 转换时间戳
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['hour'] = df['timestamp'].dt.hour

# 两列布局
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 采集数据量")
    st.metric("总记录数", len(df))

    # 按小时统计的记录数
    hourly_counts = df.groupby('hour').size().reset_index(name='count')
    fig1 = px.bar(hourly_counts, x='hour', y='count', title='各时段数据采集量')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🎯 应用使用排行")
    # 提取应用名（冒号前的部分）
    df['app_name'] = df['window_title'].apply(lambda x: x.split(':')[0] if ':' in x else x)
    app_counts = df['app_name'].value_counts().head(10).reset_index()
    app_counts.columns = ['应用', '次数']
    fig2 = px.bar(app_counts, x='次数', y='应用', orientation='h', title='最常用应用 Top 10')
    st.plotly_chart(fig2, use_container_width=True)

# 时间线视图
st.header("⏱️ 时间线视图")
df_display = df[['timestamp', 'window_title']].tail(20).sort_values('timestamp', ascending=False)
st.dataframe(df_display, use_container_width=True)

# 效率标注区域（手动标注）
st.header("✏️ 效率标注")
st.write("为未标注的数据打分（1-5分），帮助AI学习你的高效模式")

# 获取未标注的数据
conn = sqlite3.connect('learning_data.db')
unlabeled = pd.read_sql("SELECT id, timestamp, window_title FROM sessions WHERE efficiency IS NULL", conn)
conn.close()

if len(unlabeled) == 0:
    st.success("🎉 所有数据都已标注！")
else:
    st.write(f"还有 {len(unlabeled)} 条数据待标注")

    # 用session_state保存当前索引
    if 'idx' not in st.session_state:
        st.session_state.idx = 0

    if st.session_state.idx < len(unlabeled):
        row = unlabeled.iloc[st.session_state.idx]
        st.info(f"**时间**: {row['timestamp']}\n\n**窗口**: {row['window_title']}")

        col1, col2, col3, col4, col5 = st.columns(5)
        score = None
        with col1:
            if st.button("1 😞", key="b1"):
                score = 1
        with col2:
            if st.button("2 😐", key="b2"):
                score = 2
        with col3:
            if st.button("3 🤔", key="b3"):
                score = 3
        with col4:
            if st.button("4 😊", key="b4"):
                score = 4
        with col5:
            if st.button("5 🎉", key="b5"):
                score = 5

        if score:
            conn = sqlite3.connect('learning_data.db')
            c = conn.cursor()
            c.execute("UPDATE sessions SET efficiency = ? WHERE id = ?", (score, row['id']))
            conn.commit()
            conn.close()
            st.success(f"已标注为 {score} 分")
            st.session_state.idx += 1
            st.rerun()
    else:
        st.success("🎉 所有数据都已标注完成！")