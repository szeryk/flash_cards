#!/usr/bin/python3
from database_manager import *
from app_flash_cards import *


def main():
  database_name = r"flash_cards.db"
  app = FlashCardsGame(database_name)
  app.run()


if __name__ == '__main__':
    main()
