import sqlite3

__connection = None
admin = None
mail = None



def get_connection():
    global __connection
    if isinstance(__connection, object):
        __connection = sqlite3.connect("bot_database", check_same_thread=False)
    return __connection


def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()
    if force:
        c.execute("DROP TABLE IF EXISTS user_info ")
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_info (  
            id          INTEGER PRIMARY KEY,
            company_id  INTEGER NOT NULL,
            chat_id     INTEGER NOT NULL,
            name        TEXT NOT NULL,
            surname     TEXT NOT NULL,
            mail        TEXT UNIQUE,
            telephone   INTEGER NOT NULL UNIQUE,
            admin       INTEGER
            )
            """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS work_schedule (
            id          INTEGER PRIMARY KEY,
            chat_id     INTEGER NOT NULL,
            day         INTEGER,
            start_time  TEXT,
            end_time    TEXT,
            FOREIGN KEY(chat_id) REFERENCES user_info(chat_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
            )
            """)
    conn.commit()
    conn.close()


def add_reg_info_in_db(chat_id: int, company_id: int, name: str, surname: str, telephone: int, day: str,
                       start_time: str, end_time: str):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO user_info (chat_id, company_id, name, surname, telephone) VALUES (?, ?, ?, ?, ?)",
            (chat_id, company_id, name, surname, telephone))
        c.execute(
            "INSERT INTO work_schedule (chat_id, day, start_time, end_time) VALUES (?, ?, ?, ?)",
            (chat_id, day, start_time, end_time))
        conn.commit()
    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")


def update_schedule(chat_id, day, start_time, end_time):
    try:
        conn = get_connection()
        c = conn.cursor()
        print("Connected to SQLite")
        c.execute("""Update work_schedule set day = ? , start_time = ? , end_time = ? where chat_id = ?""",
                  (day, chat_id, start_time, end_time))
        conn.commit()
        print("Record Updated successfully ")
        c.close()
    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")


def update_name(chat_id, name):
    try:
        conn = get_connection()
        c = conn.cursor()
        print("Connected to SQLite")
        c.execute("""Update user_info set name = ? where chat_id = ?""", (name, chat_id))
        conn.commit()
        print("Record Updated successfully ")
        c.close()
    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")


def update_surname(chat_id, surname):
    try:
        conn = get_connection()
        c = conn.cursor()
        print("Connected to SQLite")
        c.execute("""Update user_info set surname = ? where chat_id = ?""", (surname, chat_id))
        conn.commit()
        print("Record Updated successfully ")
        c.close()
    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if conn:
            conn.close()
            print(get_connection())
            print("The SQLite connection is closed")


def update_mail(chat_id, mail):
    try:
        conn = get_connection()
        c = conn.cursor()
        print("Connected to SQLite")
        c.execute("""Update user_info set mail = ? where chat_id = ?""", (mail, chat_id))
        conn.commit()
        print("Record Updated successfully ")
        c.close()
    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")


def update_telephone(chat_id, telephone):
    try:
        conn = get_connection()
        c = conn.cursor()
        print("Connected to SQLite")
        c.execute("""Update user_info set telephone = ? where chat_id = ?""", (telephone, chat_id))
        conn.commit()
        print("Record Updated successfully ")
        c.close()
    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")


def admin_check(chat_id):
    global admin
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT admin FROM user_info WHERE chat_id = ?", (chat_id,))
        admin = c.fetchone()
        c.close()
    except sqlite3.Error as error:
        print("Failed to read single row from sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")
    return admin[0]


def mail_check(chat_id):
    global mail
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT mail FROM user_info WHERE chat_id = ?", (chat_id,))
        mail = c.fetchone()
        c.close()
    except sqlite3.Error as error:
        print("Failed to read single row from sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")
    return mail[0]


def fromCompanyId_adminCheck(company_id):
    global mail
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT mail FROM user_info WHERE company_id = ? and admin=1", (company_id,))
        mail = c.fetchone()
        c.close()
    except sqlite3.Error as error:
        print("Failed to read single row from sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")
    return mail[0]