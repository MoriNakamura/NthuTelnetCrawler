import sqlite3
import re


def dataCleaner():
    sqlite = sqlite3.connect('nthu_course.db')
    cur = sqlite.cursor()

    cur.execute('')

    for row in cur.execute('SELECT * FROM Raw_Data WHERE aid = 2;'):
        str = row[1].decode("utf8", "ignore")
        print(str)

        print('\n\n\n\n\n')
        ansi_escape = re.compile(r'\x1b\[\d{1,2};1H')
        ansi_escape2 = re.compile(r'\x1b\[\d*K')
        ansi_escape3 = re.compile(r'\x1b[^mH]*[mH]')

        str = ansi_escape.sub('\n', str)
        str = ansi_escape2.sub('', str)
        str = ansi_escape3.sub('', str)
        print(str)



