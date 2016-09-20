import sqlite3
import re
import sys


def strip_first_line(str):
    return str[str.find("\n") + 1:]


def store_push(cur, article_id, push_boo, pusher, push_content, push_time):
    cur.execute('INSERT INTO pushes(article_id, push_boo, pusher, content, published_time) values (?,?,?,?,?);',
                (article_id, push_boo, pusher, push_content, push_time))



def data_cleaner():
    sqlite = sqlite3.connect('nthu_course.db')
    cur = sqlite.cursor()
    cur2 = sqlite.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY, title TEXT NOT NULL, '
                ' author TEXT NOT NULL, author_nickname TEXT NOT NULL, category TEXT, content TEXT NOT NULL, is_reply INTEGER NOT NULL,'
     'push_score INTEGER NOT NULL, published_time TEXT NOT NULL);')

    cur.execute('CREATE TABLE IF NOT EXISTS pushes (id INTEGER PRIMARY KEY, article_id INTEGER, '
    'push_boo INTEGER NOT NULL, pusher TEXT NOT NULL, content TEXT NOT NULL, published_time TEXT NOT NULL,'
    ' FOREIGN KEY(article_id) REFERENCES articles(id) ON UPDATE CASCADE);')



    re_ansi_escape = re.compile(r'\x1b\[\d{1,2};1H')
    re_ansi_escape2 = re.compile(r'\x1b\[\d*K')
    re_ansi_escape3 = re.compile(r'\x1b[^mH]*[mH]')
    re_pushtime = re.compile(r'\d\d/\d\d \d\d:\d\d')
    re_end = re.compile(r' *\n')

    for row in cur.execute('SELECT * FROM Raw_Data;'):
        try:
            print(row[0])
            str = row[1].decode("utf8", "ignore")

            str = re_ansi_escape.sub('\n', str)
            str = re_ansi_escape2.sub('', str)
            str = re_ansi_escape3.sub('', str)
            str = re.sub(r'\r', '', str)
            #
            # if row[0] == 1:
            #     str = strip_first_line(str)

            author = str[str.find("作者  ", 0, 10)+4: str.find(" (", 0, 40)]
            nickname = str[str.find(" (", 0, 40)+2: str.find(")")]

            str = strip_first_line(str)

            title = str[str.find("標題  ")+4: re_end.search(str).start()]

            if '[' in title:
                category = title[title.find('[')+1:title.find(']')]
            else:
                category = ""

            str = strip_first_line(str)

            time = str[str.find("時間  ")+4: re_end.search(str).start()]

            str = strip_first_line(strip_first_line(str))

            content = str[: str.find("--\n")]

            if "Re: " in title:
                is_reply = 1
            else:
                is_reply = 0

            # Skip to pushes

            str = str[str.find("--\n")+3: ]

            while str and str[0] != "△" and str[0] != "─" and str[0] != "▽":
                str = strip_first_line(str)

            push = str.count("△") - str.count("▽")

            cur2.execute('INSERT INTO articles(title, author, author_nickname, category, content, is_reply, push_score, published_time)'
                         ' VALUES (?,?,?,?,?,?,?,?);', (title, author, nickname, category, content, is_reply, push, time))

            pusher = ""
            push_content = ""
            push_time = ""



            while str:
                if str[0] == "△" or str[0] == "─" or str[0] == "▽":
                    if pusher:
                        store_push(cur2, row[0], push_boo, pusher, push_content, push_time)
                    pusher = ""

                    push_content = ""
                    if str[0] == "△":
                        push_boo = 1
                    elif str[0] == "▽":
                        push_boo = -1
                    else:
                        push_boo = 0

                    pusher = str[str.find(" ")+1: str.find("：")]
                    pushtime_match = re_pushtime.search(str)
                    push_time = pushtime_match.group(0)
                    push_content = str[str.find("：")+1: pushtime_match.start()]

                elif str[0] == " ":
                    push_content += str[re.search(" *", str).end()+1: re_end.search(str).start()]

                else:
                    if pusher:
                        store_push(cur2, row[0], push_boo, pusher, push_content, push_time)
                        pusher = ""

                str = strip_first_line(str)

            if pusher:
                store_push(cur2, row[0], push_boo, pusher, push_content, push_time)

            if row[0] % 200 == 0:
                print(row[0])
                sqlite.commit()

        except:
            print(sys.exc_info()[0])

    sqlite.commit()















