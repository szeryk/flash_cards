import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

#    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_new_questions_database(db_file):

    sql = """ CREATE TABLE IF NOT EXISTS questions (
        id integer PRIMARY KEY,
        polish text NOT NULL,
        english text NOT NULL
        ); """
    conn = create_connection(db_file)
    with conn:
        create_table(conn, sql)


def add_question(conn, question):
    print("Adding question: " + str(question))
    sql = ''' INSERT INTO questions(polish,english)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, question)
    conn.commit()

    return cur.lastrowid


def update_question(conn, question):
    sql = ''' UPDATE questions
              SET polish = ? ,
                  english = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, question)
    conn.commit()


def delete_question(conn, id):
    sql = 'DELETE FROM questions WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()


def show_questions(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions")

    rows = cur.fetchall()
    for row in rows:
        print(row)
