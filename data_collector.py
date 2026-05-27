# data_collector.py
import time
import sqlite3
import datetime
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID

def get_active_window():
    """获取Mac当前活动窗口名称"""
    options = kCGWindowListOptionOnScreenOnly
    window_list = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
    for window in window_list:
        # 只取最前层的窗口
        if window.get('kCGWindowLayer') == 0:
            owner = window.get('kCGWindowOwnerName', 'Unknown')
            name = window.get('kCGWindowName', '')
            # 如果窗口标题为空，只显示应用名
            if name:
                return f"{owner}: {name}"
            else:
                return owner
    return "Unknown"

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect('learning_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sessions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  window_title TEXT,
                  efficiency INTEGER)''')
    conn.commit()
    conn.close()
    print("数据库初始化完成")

def collect_one_record():
    """采集一条数据"""
    conn = sqlite3.connect('learning_data.db')
    c = conn.cursor()
    now = datetime.datetime.now().isoformat()
    window = get_active_window()
    # efficiency先留空，后续手动标注
    c.execute("INSERT INTO sessions (timestamp, window_title, efficiency) VALUES (?, ?, ?)",
              (now, window, None))
    conn.commit()
    conn.close()
    print(f"已记录: {now} | {window}")

def continuous_collect(interval_seconds=60):
    """持续采集，interval_seconds为采集间隔（秒）"""
    print(f"开始持续采集，每{interval_seconds}秒记录一次")
    print("按 Ctrl+C 停止\n")
    try:
        while True:
            collect_one_record()
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\n采集已停止")

if __name__ == "__main__":
    import sys
    
    # 检查是否有 --continuous 参数
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        init_db()
        continuous_collect()
    else:
        init_db()
        collect_one_record()
        print("测试完成！如果要持续采集，请运行: python data_collector.py --continuous")