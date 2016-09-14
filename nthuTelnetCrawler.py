import telnetlib
import getpass
import time

# 楓橋
SITE_IP = 'bbs.cs.nthu.edu.tw'
USER_ID = 'MoriNakamura'
password = 'iamfrank'

# connecting
tn = telnetlib.Telnet(SITE_IP)

# log in
content = tn.read_until("[您的帳號]".encode('big5'), 5)
tn.write(USER_ID.encode('ascii') + b"\n")
tn.read_until("[您的密碼]".encode('big5'), 5)
tn.write(password.encode('ascii') + b"\n")

# skip some pages
content = tn.read_until("繼續 ●".encode('big5'), 1).decode('big5','ignore')
tn.write(b"\n")
content = tn.read_until("繼續 ●".encode('big5'), 1).decode('big5','ignore')
tn.write(b"\n")
content = tn.read_until("繼續 ●".encode('big5'), 1).decode('big5','ignore')
tn.write(b"\n")
content = tn.read_until("繼續 ●".encode('big5'), 1).decode('big5','ignore')
tn.write(b"\n")
content = tn.read_until("(h)說明".encode('big5'), 1).decode('big5','ignore')

# go to nthu.course

tn.write(b"s")
content = tn.read_until("自動搜尋)：".encode('big5'), 1).decode('big5','ignore')
tn.write(b"nthu.course\n")

content = tn.read_until("繼續 ●".encode('big5'), 1).decode('big5','ignore')
tn.write(b"\n")

# go to the first article

content = tn.read_until("/新聞".encode('big5'), 1).decode('big5','ignore')
tn.write(b"1")

content = tn.read_until("第幾項：".encode('big5'), 1).decode('big5','ignore')
tn.write(b"\n")

content = tn.read_until("/新聞".encode('big5'), 1).decode('big5','ignore')

print(len(content))

print(content)
