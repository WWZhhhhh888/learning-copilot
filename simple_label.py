import sqlite3
import streamlit as st

st.title("效率标注")

conn = sqlite3.connect('learning_data.db')
c = conn.cursor()

# 获取未标注的一条
c.execute("SELECT id, timestamp, window_title FROM sessions WHERE efficiency IS NULL LIMIT 1")
row = c.fetchone()

if row:
    st.write(f"ID: {row[0]}")
    st.write(f"时间: {row[1]}")
    st.write(f"窗口: {row[2]}")
    
    score = st.selectbox("效率评分", [1,2,3,4,5], format_func=lambda x: {1:"1-很低效",2:"2-较低效",3:"3-一般",4:"4-高效",5:"5-非常高效"}[x])
    
    if st.button("保存"):
        c.execute("UPDATE sessions SET efficiency = ? WHERE id = ?", (score, row[0]))
        conn.commit()
        st.success("已保存！刷新页面继续下一条")
        st.rerun()
else:
    st.success("全部标注完成！")

conn.close()

