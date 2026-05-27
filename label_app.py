# label_app.py - 简化可靠的标注工具
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="效率标注工具", layout="wide")

st.title("✏️ 学习效率标注工具")

# 初始化数据库连接
conn = sqlite3.connect('learning_data.db')
c = conn.cursor()

# 获取未标注的数据
df = pd.read_sql("SELECT id, timestamp, window_title FROM sessions WHERE efficiency IS NULL ORDER BY timestamp DESC", conn)

if len(df) == 0:
    st.success("🎉 所有数据都已标注完成！")
    st.stop()

st.write(f"### 还有 {len(df)} 条数据待标注")

# 用session_state记录当前索引
if 'idx' not in st.session_state:
    st.session_state.idx = 0

if st.session_state.idx < len(df):
    row = df.iloc[st.session_state.idx]
    
    st.info(f"""
    **时间**: {row['timestamp']}
    
    **窗口**: {row['window_title']}
    """)
    
    st.write("#### 当时的学习效率：")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    if col1.button("1 😞 很低效", key="b1", use_container_width=True):
        c.execute("UPDATE sessions SET efficiency = 1 WHERE id = ?", (row['id'],))
        conn.commit()
        st.session_state.idx += 1
        st.rerun()
        
    if col2.button("2 😐 较低效", key="b2", use_container_width=True):
        c.execute("UPDATE sessions SET efficiency = 2 WHERE id = ?", (row['id'],))
        conn.commit()
        st.session_state.idx += 1
        st.rerun()
        
    if col3.button("3 🤔 一般", key="b3", use_container_width=True):
        c.execute("UPDATE sessions SET efficiency = 3 WHERE id = ?", (row['id'],))
        conn.commit()
        st.session_state.idx += 1
        st.rerun()
        
    if col4.button("4 😊 高效", key="b4", use_container_width=True):
        c.execute("UPDATE sessions SET efficiency = 4 WHERE id = ?", (row['id'],))
        conn.commit()
        st.session_state.idx += 1
        st.rerun()
        
    if col5.button("5 🎉 非常高效", key="b5", use_container_width=True):
        c.execute("UPDATE sessions SET efficiency = 5 WHERE id = ?", (row['id'],))
        conn.commit()
        st.session_state.idx += 1
        st.rerun()
    
    # 显示进度
    st.progress(st.session_state.idx / len(df))
    st.write(f"进度: {st.session_state.idx}/{len(df)}")
    
else:
    st.success("🎉 恭喜！所有数据标注完成！")
    conn.close()

# 显示已标注统计
conn2 = sqlite3.connect('learning_data.db')
labeled = pd.read_sql("SELECT COUNT(*) as count FROM sessions WHERE efficiency IS NOT NULL", conn2)
total = pd.read_sql("SELECT COUNT(*) as count FROM sessions", conn2)
st.sidebar.write(f"### 📊 统计")
st.sidebar.write(f"已标注: {labeled['count'].iloc[0]} 条")
st.sidebar.write(f"总计: {total['count'].iloc[0]} 条")
st.sidebar.write(f"进度: {labeled['count'].iloc[0]/total['count'].iloc[0]*100:.1f}%")
conn2.close()