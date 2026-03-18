def init_database():
    """初始化数据库"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS recognition_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            face_id INTEGER NOT NULL,
            confidence REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_log(face_id, confidence):
    """插入识别记录到数据库"""
    conn = sqlite3.connect(DATABASE)  # 每次插入创建新连接
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO recognition_log (face_id, confidence) VALUES (?, ?)
    ''', (face_id, confidence))
    conn.commit()
    conn.close()