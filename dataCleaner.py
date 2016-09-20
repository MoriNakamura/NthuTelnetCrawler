import sqlite3
import re


def strip_first_line(str):
    return str[str.find("\n") + 1:]


def store_push(pusher, push_content, push_time):
    print(pusher)
    print(push_content)
    print(push_time)


def data_cleaner():
    sqlite = sqlite3.connect('nthu_course.db')
    cur = sqlite.cursor()

    cur.execute('')

    re_ansi_escape = re.compile(r'\x1b\[\d{1,2};1H')
    re_ansi_escape2 = re.compile(r'\x1b\[\d*K')
    re_ansi_escape3 = re.compile(r'\x1b[^mH]*[mH]')
    re_pushtime = re.compile(r'\d\d/\d\d \d\d:\d\d')
    re_end = re.compile(r' *\n')

    for row in cur.execute('SELECT * FROM Raw_Data WHERE aid = 2;'):
        str = row[1].decode("utf8", "ignore")

        str = re_ansi_escape.sub('\n', str)
        str = re_ansi_escape2.sub('', str)
        str = re_ansi_escape3.sub('', str)
        str = re.sub(r'\r', '', str)

        author = str[str.find("作者  ", 0, 10)+4: str.find(" (", 0, 40)]
        nickname = str[str.find(" (", 0, 40)+2: str.find(")")]

        str = strip_first_line(str)

        title = str[str.find("標題  ")+4: re_end.search(str).start()]


        str = strip_first_line(str)

        time = str[str.find("時間  ")+4: re_end.search(str).start()]

        str = strip_first_line(strip_first_line(str))

        content = str[: str.find("--\n")]

        # Skip to pushes

        str = str[str.find("--\n")+3: ]

        while str[0] != "△" and str[0] != "─" and str[0] != "▽":
            str = strip_first_line(str)

        push = 0;
        pusher = ""
        push_content = ""
        push_time = ""

        while str:
            if str[0] == "△" or str[0] == "─" or str[0] == "▽":
                if pusher:
                    store_push(pusher, push_content, push_time)

                push_content = ""
                if str[0] == "△":
                    push += 1
                if str[0] == "▽":
                    push -= 1

                pusher = str[str.find(" ")+1: str.find("：")]
                pushtime_match = re_pushtime.search(str)
                push_time = pushtime_match.group(0)
                push_content = str[str.find("：")+1: pushtime_match.start()]

            elif str[0] == " ":
                push_content += str[re.search(" *", str).end()+1: re_end.search(str).start()]

            else:
                if pusher:
                    store_push(pusher, push_content, push_time)

            str = strip_first_line(str)

        if pusher:
            store_push(pusher, push_content, push_time)
















