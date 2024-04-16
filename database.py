import sqlite3


def database():
    conn = sqlite3.connect(database=r'idata.db')
    print("Opened database successfully")
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS employee (eid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, gender TEXT,"
                " contact TEXT, dob TEXT, doj TEXT, email TEXT, pass TEXT, utype TEXT, address TEXT, salary TEXT)")
    conn.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS supplier (invoice INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, "
                "description TEXT, contact TEXT)")
    conn.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS category (cid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    conn.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS product (pid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, category TEXT,"
                "supplier TEXT, price TEXT, quantity TEXT, status TEXT)")
    conn.commit()

    conn.close()

    print("Table created successfully")


database()
