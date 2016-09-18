import sqlite3

sqlite = sqlite3.connect('nthu_course.db')
cur = sqlite.cursor()

cur.execute('')

for row in cur.execute('SELECT * FROM Raw_Data'):
    