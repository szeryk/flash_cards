import sqlite3
import os.path

class DatabaseManager:
  def __init__(self, db_file_name: str):

    self.db_file = db_file_name
    if not os.path.isfile(self.db_file):
      print("Database not found in current directory! Creating a new one.")
      self.create_new_questions_database()
    else:
      self.create_connection()


  def __del__(self):
    self.conn.close()

  
  def sql_transaction(self, sql_command: str, *args) -> None:
    with self.conn:
      try:
        cur = self.conn.cursor()
        cur.execute(sql_command, *args)
      except sqlite3.Error as e:
        print(e)
      return cur.fetchall()


  def create_connection(self) -> None:
    conn = None
    try:
      conn = sqlite3.connect(self.db_file)
    except sqlite3.Error as e:
      print(e)
    self.conn = conn
  
  
  def create_new_questions_database(self) -> None:
    sql = """ CREATE TABLE IF NOT EXISTS questions (
        id integer PRIMARY KEY,
        polish text NOT NULL,
        english text NOT NULL
        ); """
    self.create_connection()
    self.sql_transaction(sql)

  
  def add_question(self, polish: str, english: str) -> None:
    sql = ''' INSERT INTO questions(polish,english)
              VALUES(:polish,:english) '''
    self.sql_transaction(sql, {'polish': polish, 'english': english})
  
  
  def update_question(self, id: str, polish: str, english: str) -> None:
    sql = ''' UPDATE questions
              SET polish = :polish ,
                  english = :english
              WHERE id = :id'''
    self.sql_transaction(sql, {'polish': polish, 'english': english, 'id': id})
  
  
  def delete_question(self, id: str) -> None:
    sql = 'DELETE FROM questions WHERE id = :id'
    self.sql_transaction(sql, {'id': int(id)})
  
  
  def show_questions(self) -> None:
    sql = "SELECT * FROM questions"
    rows = self.sql_transaction(sql) 
    for row in rows:
      print(row)
  
  
  def get_database_questions_count(self) -> int:
    sql = 'SELECT Count(*) FROM questions'
    count = self.sql_transaction(sql)[0][0]
    return count


  def get_random_question(self) -> tuple:
    sql = 'SELECT * FROM questions ORDER BY RANDOM() LIMIT 1'
    row = self.sql_transaction(sql)[0]
    return row
