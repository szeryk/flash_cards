import database
import os.path
from app_flash_cards import *


def main():

  dbfile = r"flash_cards.db"

  if not os.path.isfile(dbfile):
    print("Database not found in current directory! Creating a new one.")
    database.create_new_questions_database(dbfile)

  conn = database.create_connection(dbfile)
  app = FlashCardsGame(conn)
  app.run()


if __name__ == '__main__':
    main()
