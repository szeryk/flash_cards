from database_manager import *


class FlashCardsGame:
  def __init__(self, database_name: str):
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

    self.db_manager.add_question(polish=words[1], english=words[2])


  def delete_command(self, words: list) -> None:
    if len(words) < 2:
      print("Not enough arguments!")
      return

    self.db_manager.delete_question(id=words[1])


  def update_command(self, words: list) -> None:
    if len(words) < 4:
      print("Not enough arguments!")
      return

    self.db_manager.update_question(id=words[1], polish=words[2], english=words[3])


  def show_command(self) -> None:
    questions = self.db_manager.get_all_questions()
    for q in questions:
      print(q)


  def parse_user_commands(self) -> bool:
    '''Parse user commands. Return False if user wants to quit the app.'''

    command = input(self.PROMPT)

    words = command.split()
    if words[0] == 'help':
      self.print_help()

    elif words[0] == 'add':
      self.add_command(words)
      self.show_command()

    elif words[0] == 'show':
      self.show_command()

    elif words[0] == 'delete':
      self.delete_command(words)
      self.show_command()

    elif words[0] == 'update':
      self.update_command(words)
      self.show_command()

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

    if self.db_manager.get_questions_count() < 1:
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
        user_input = input("Translate: " + polish + "\n" + self.PROMPT)
        if user_input == english:
          good_answers += 1
          asked_questions += 1
          break
        elif user_input == 'IamStupid':
          print("The answer is: " + english)
        elif user_input == 'quit':
          print("Game over :) You asked properly " + str(good_answers) + " out of " + str(asked_questions) + " questions.")
          return
        else:
          print("Nope :( Try again. Write: IamStupid - to check the answer, quit - to quit.")
          asked_questions += 1


  def run(self) -> None:
    ''' Run application in endless loop'''
    self.print_help()
    while self.parse_user_commands():
      pass
