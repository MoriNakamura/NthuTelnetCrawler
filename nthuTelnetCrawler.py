import telnetlib
import sqlite3
import getpass
import time

def nthuTelnetCrawler():
    # Some constants
    RIGHT = b"\x1b[C"
    LEFT = b"\x1b[D"
    UP = b"\x1b[A"
    DOWN = b"\x1b[B"
    ENTER = b"\n"

    # 楓橋
    SITE_IP = 'bbs.cs.nthu.edu.tw'
    USER_ID = 'MoriNakamura'
    password = 'iamfrank'

    # SQlite
    sqlite = sqlite3.connect('nthu_course.db')
    cur = sqlite.cursor()

    # connecting
    tn = telnetlib.Telnet(SITE_IP)

    # log in
    content = tn.read_until("[您的帳號]".encode('big5'), 5)
    tn.write(USER_ID.encode('ascii') + ENTER)
    tn.read_until("[您的密碼]".encode('big5'), 5)
    tn.write(password.encode('ascii') + ENTER)

    # skip some pages
    # content = tn.read_until("？[Y]".encode('big5'), 1).decode('big5', 'ignore')
    # tn.write(b'n')
    # tn.write(ENTER)
    content = tn.read_until("繼續 ●".encode('big5'), 1).decode('big5', 'ignore')
    tn.write(ENTER)
    content = tn.read_until("繼續 ●".encode('big5'), 1).decode('big5', 'ignore')
    tn.write(ENTER)
    content = tn.read_until("繼續 ●".encode('big5'), 1).decode('big5', 'ignore')
    tn.write(ENTER)
    content = tn.read_until("繼續 ●".encode('big5'), 1).decode('big5', 'ignore')
    tn.write(ENTER)
    content = tn.read_until("(h)說明".encode('big5'), 1).decode('big5', 'ignore')

    # go to nthu.course

    tn.write(b"s")
    content = tn.read_until("自動搜尋)：".encode('big5'), 1).decode('big5','ignore')
    tn.write(b"nthu.course\n")

    content = tn.read_until("繼續 ●".encode('big5'), 1).decode('big5', 'ignore')
    tn.write(ENTER)

    # go to the first article

    content = tn.read_until("/新聞".encode('big5'), 1).decode('big5', 'ignore')
    tn.write(b"1\n")
    content = tn.read_until("/新聞".encode('big5'), 1).decode('big5', 'ignore')

    # Iterate through all posts
    # for i in range(0,13220):
    for i in range(0, 13220):
        if i % 20 == 0:
            print(i, "\n")
            sqlite.commit()
        content = ""
        tn.write(RIGHT)
        while True:
            str = ''
            while not str:
                response = tn.expect([b'(\xa1\xf6q)'], 0.13)
                str = response[2].decode('big5', 'ignore')
                str = str.lstrip('\r\n')
                if "搜尋標題作者" in str or "動畫播放" in str:
                    str = str[:str.rfind('\n')]
                str += '\n'
            content += str
            tn.read_until(b"stbhrsbs", 0.02)
            if response[0] != 0:
                # print(content)
                # Store into raw data db
                cur.execute('INSERT INTO Raw_Data(content) VALUES (?);', (content.encode("utf8", "ignore"),))
                break
            tn.write(RIGHT)
        # print(content)
        # print("---------")

    sqlite.commit()

    # content = tn.read_until("/新聞".encode('big5'), 1).decode('big5','ignore')
    #
    # print(content)
    #
    # tn.write(RIGHT)
    # content = tn.read_until("(←q)".encode('big5'), 3).decode('big5','ignore')
    #
    # print(len(content))
    #
    # print(content)
    #
    # tn.write(RIGHT)
    # content = tn.read_until("/新聞".encode('big5'), 1).decode('big5','ignore')
    #
    # print(len(content))
    #
    # print(content)
