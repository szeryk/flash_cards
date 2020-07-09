from database_manager import *


class FlashCardsGame:
  def __init__(self, database_name):
    self.db_manager = DatabaseManager(database_name)
    self.PROMPT = "> "


  def print_help(self) -> None:
    help = '''
           What you want to do?
           To see help again: help
           To add a question: add polish_word english_translation
           To show your questions: show
           To delete a question: delete id
           To update a question: update id polish_word english_translation
           To play: play
           To clear screen: clear
           To quit: quit\n'''
    print(help)


  def add_command(self, words: list) -> None:
    if len(words) < 3:
      print("Not enough arguments!")
      return

    self.db_manager.add_question(words[1], words[2])
    self.db_manager.show_questions()


  def delete_command(self, words: list) -> None:
    if len(words) < 2:
      print("Not enough arguments!")
      return

    self.db_manager.delete_question(words[1])
    self.db_manager.show_questions()


  def update_command(self, words: list) -> None:
    if len(words) < 4:
      print("Not enough arguments!")
      return

    self.db_manager.update_question(words[1], words[2], words[3])
    self.db_manager.show_questions()


  def parse_commands(self) -> bool:
    '''Parse user commands. Return False if user wants to quit the app.'''

    command = input(self.PROMPT)

    words = command.split()
    if words[0] == 'help':
      self.print_help()

    elif words[0] == 'add':
      self.add_command(words)

    elif words[0] == 'show':
      self.db_manager.show_questions()

    elif words[0] == 'delete':
      self.delete_command(words)

    elif words[0] == 'update':
      self.update_command(words)

    elif words[0] == 'quit':
      return False

    elif words[0] == 'play':
      self.play()
      self.print_help()

    elif words[0] == 'clear':
      for i in range(100):
        print('\n')

    return True


  def play(self) -> None:
    ''' Play the flash cards game until user inputs "quit" '''

    if self.db_manager.get_database_questions_count() < 1:
      print("Cannot play! No questions in database!")
      return

    print("I will give you a polish word, you must provide an english translation. To exit write: quit. Let's go!\n")
    good_answers = 0
    asked_questions = 0

    while True:
      question = self.db_manager.get_random_question()
      polish = question[1]
      english = question[2]

      while True:
        i = input("Translate: " + polish + "\n" + self.PROMPT)
        if i == english:
          good_answers += 1
          asked_questions += 1
          break
        elif i == 'IamStupid':
          print("The answer is: " + english)
        elif i == 'quit':
          print("Game over :) You asked properly " + str(good_answers) + " out of " + str(asked_questions) + " questions.")
          return
        else:
          print("Nope :( Try again. Write: IamStupid - to check the answer, quit - to quit.")
          asked_questions += 1


  def run(self) -> None:
    ''' Run application in endless loop'''
    self.print_help()
    while self.parse_commands():
      pass
