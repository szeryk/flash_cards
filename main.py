import database


def play(conn):
    print("I will give you polish word, you must provide english translation. To exit write: quit. Let's go!\n")
    sql = 'SELECT * FROM questions ORDER BY RANDOM() LIMIT 1'
    cur = conn.cursor()
    good_answers = 0
    asked_questions = 1

    while True:
        cur.execute(sql)
        row = cur.fetchall()[0]
        question = row[1]
        answer = row[2]

        while True:
            i = input("Translate: " + question + "\n> ")
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


def main():
    # create a database connection
    #conn = database.create_new_questions_database(dbfile)

    user = input("Who is using the program? Write: kejty or eryk\n> ")
    if user == 'kejty':
        dbfile = r"kejty.db"
    elif user == 'eryk':
        dbfile = r"eryk.db"
    else:
        print("you written somewthing else..... bye")
        exit(0)

    conn = database.create_connection(dbfile)

    with conn:

        help = '''
            What you want to do?
            To see help again: help
            To add a question: add polish english
            To show your questions: show
            To delete a question: delete id
            To update a question: update polish english id
            To play: play
            To clear screen: clear
            To quit: quit\n'''

        print(help)
        while True:
            command = input('> ')

            if command == "":
                continue

            words = command.split()
            if words[0] == 'help':
                print(help)
            elif words[0] == 'add':
                question = (words[1], words[2])
                database.add_question(conn, question)
                database.show_questions(conn)
            elif words[0] == 'show':
                database.show_questions(conn)
            elif words[0] == 'delete':
                database.delete_question(conn, int(words[1]))
                database.show_questions(conn)
            elif words[0] == 'update':
                question = (words[1], words[2], words[3])
                database.update_question(conn, question)
                database.show_questions(conn)
            elif words[0] == 'quit':
                break
            elif words[0] == 'play':
                play(conn)
                print(help)
            elif words[0] == 'clear':
                for i in range(100):
                    print('\n')
            else:
                continue

            if command == "":
                continue


if __name__ == '__main__':
    main()