import sqlite3
import datetime

def data_select():
    sqlite = sqlite3.connect('nthu_course.db')
    cur = sqlite.cursor()

    for row in cur.execute("SELECT content FROM articles;"):
        # if "推薦" in row[0] or "大推" in row[0] or "認真" in row[0] or "用心" or "好課" in row[0]:
        if "不建議" in row[0] or "不推" in row[0] or "雷" in row[0] or "無聊" in row[0]:
            print(row[0])
            input("-------------------------------------------")