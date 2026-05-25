import os
import sqlite3
import pymysql
from dotenv import load_dotenv

load_dotenv()

try:
    sqlite_conn = sqlite3.connect("tech0_search.db")
    sqlite_conn.row_factory = sqlite3.Row
    rows = sqlite_conn.execute("SELECT title, url, body FROM pages").fetchall()
    print(f"SQLite件数: {len(rows)}")
    mysql_conn = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        charset="utf8mb4",
        ssl={"ssl_disabled": False}
    )
    print("MySQL接続成功!")
    cursor = mysql_conn.cursor()
    for row in rows:
        cursor.execute("INSERT IGNORE INTO pages (title, url, body) VALUES (%s, %s, %s)", (row["title"], row["url"], row["body"]))
    mysql_conn.commit()
    print(f"移行完了: {len(rows)}件")
except Exception as e:
    print(f"エラー: {e}")