import sqlite3


def manual_data_cleaner():
    sqlite = sqlite3.connect('nthu_course.db')
    cur = sqlite.cursor()
    cur2 = sqlite.cursor()
    categories = []

    for row in cur.execute("SELECT id, category FROM articles;"):
        # print(row[0])
        # if row[1].startswith(""):
        #     cur2.execute("UPDATE articles SET category = '問題' WHERE id = (?);", (row[0],))
        #     sqlite.commit()
        if row[1] not in categories:
            print(row[1])
            categories.append(row[1])

    print(categories)
