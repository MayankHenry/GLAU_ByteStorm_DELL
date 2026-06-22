import sqlite3
from datetime import datetime

def init_db(db_name="threat_logs.db"):
    """Initializes the SQLite database for persistent threat tracking."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            srcip TEXT,
            severity TEXT,
            total_connections INTEGER,
            unique_ports INTEGER,
            exfiltration_risk BOOLEAN,
            critical_targets BOOLEAN
        )
    ''')
    conn.commit()
    return conn

def log_incidents(df):
    """Saves flagged suspicious IPs to the database."""
    conn = init_db()
    cursor = conn.cursor()
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO incidents (timestamp, srcip, severity, total_connections, unique_ports, exfiltration_risk, critical_targets)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            current_time, row['srcip'], row['severity'], 
            row['total_connections'], row['unique_dst_ports'], 
            row['exfiltration_risk'], row['critical_targets']
        ))
    
    conn.commit()
    conn.close()
    print("[+] Incident data securely logged to local SQLite database (threat_logs.db).")