import database

class FlashCardsGame:
  def __init__(self, conn):
    self.conn = conn
    self.PROMPT = "> "


  def print_help(self):
    help = '''
           What you want to do?
           To see help again: help
           To add a question: add polish_word english_translation
           To show your questions: show
           To delete a question: delete id
           To update a question: update polish_word english_translation id
           To play: play
           To clear screen: clear
           To quit: quit\n'''

    print(help)


  def parse_commands(self):
    '''Parse user commands. Return False if user wants to quit the app.'''

    command = input(self.PROMPT)

    words = command.split()
    if words[0] == 'help':
      self.print_help()
    elif words[0] == 'add':
      question = (words[1], words[2])
      database.add_question(self.conn, question)
      database.show_questions(self.conn)
    elif words[0] == 'show':
      database.show_questions(self.conn)
    elif words[0] == 'delete':
      database.delete_question(self.conn, int(words[1]))
      database.show_questions(self.conn)
    elif words[0] == 'update':
      question = (words[1], words[2], words[3])
      database.update_question(self.conn, question)
      database.show_questions(self.conn)
    elif words[0] == 'quit':
      return False
    elif words[0] == 'play':
      self.play()
      self.print_help()
    elif words[0] == 'clear':
      for i in range(100):
        print('\n')

    return True


  def play(self):
    ''' Play the flash cards game until user inputs "quit" '''

    if database.get_database_questions_count(self.conn) < 1:
      print("Cannot play! No questions in database!")
      return

    print("I will give you a polish word, you must provide an english translation. To exit write: quit. Let's go!\n")
    sql = 'SELECT * FROM questions ORDER BY RANDOM() LIMIT 1'
    cur = self.conn.cursor()
    good_answers = 0
    asked_questions = 0

    while True:
      cur.execute(sql)
      row = cur.fetchall()[0]
      question = row[1]
      answer = row[2]

      while True:
        i = input("Translate: " + question + "\n" + self.PROMPT)
        if i == answer:
          good_answers += 1
          asked_questions += 1
          break
        elif i == 'IamStupid':
          print("The answer is: " + answer )
        elif i == 'quit':
          print("Game over :) You asked properly " + str(good_answers) + " out of " + str(asked_questions) + " questions.")
          return
        else:
          print("Nope :( Try again. Write: IamStupid - to check the answer, quit - to quit.")
          asked_questions += 1


  def run(self):
    self.print_help()
    while self.parse_commands():
      pass
