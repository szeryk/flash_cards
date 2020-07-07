import sqlite3
import os.path

class DatabaseManager:
  def __init__(self, db_file_name):

    self.db_file = db_file_name
    if not os.path.isfile(self.db_file):
      print("Database not found in current directory! Creating a new one.")
      self.create_new_questions_database()
    else:
      self.create_connection()


  def create_connection(self):
    conn = None

    try:
      conn = sqlite3.connect(self.db_file)
    except sqlite3.Error as e:
      print(e)

    self.conn = conn
  
  
  def create_new_questions_database(self):
    sql = """ CREATE TABLE IF NOT EXISTS questions (
        id integer PRIMARY KEY,
        polish text NOT NULL,
        english text NOT NULL
        ); """
    self.create_connection()

    try:
      c = self.conn.cursor()
      c.execute(sql)
    except sqlite3.Error as e:
      print(e)

  
  def add_question(self, question):
    print("Adding question: " + str(question))
    sql = ''' INSERT INTO questions(polish,english)
              VALUES(?,?) '''
    cur = self.conn.cursor()
    cur.execute(sql, question)
    self.conn.commit()
  
  
  def update_question(self, question):
    sql = ''' UPDATE questions
              SET polish = ? ,
                  english = ?
              WHERE id = ?'''
    cur = self.conn.cursor()
    cur.execute(sql, question)
    self.conn.commit()
  
  
  def delete_question(self, id):
    sql = 'DELETE FROM questions WHERE id=?'
    cur = self.conn.cursor()
    cur.execute(sql, (id,))
    self.conn.commit()
  
  
  def show_questions(self):
    cur = self.conn.cursor()
    cur.execute("SELECT * FROM questions")
    rows = cur.fetchall()
    for row in rows:
      print(row)
  
  
  def get_database_questions_count(self):
    sql = 'SELECT Count(*) FROM questions'
    cur = self.conn.cursor()
    cur.execute(sql)
    count = cur.fetchall()[0][0]
    return count


  def get_random_row(self):
    sql = 'SELECT * FROM questions ORDER BY RANDOM() LIMIT 1'
    cur = self.conn.cursor()
    cur.execute(sql)
    row = cur.fetchall()[0]
    return row
