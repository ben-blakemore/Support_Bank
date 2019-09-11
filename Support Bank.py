import csv
import json
import logging
import time
import os
from datetime import datetime
from datetime import timedelta
import xml.etree.ElementTree as et
from FileParser import FileParser
from User import User
from Transactions import Transactions


def fail(message):
    current_time = time.ctime()
    logging.info(f"[{current_time}] {message}")
    print(f"[{current_time}] {message}")


def process_line(users, transactions, line):
    payer = line[1]
    payee = line[2]

    if payer.lower() not in users:
        users[payer.lower()] = User(payer)
    if payee.lower() not in users:
        users[payee.lower()] = User(payee)
    try:
        transactions.append(Transactions(line))
        users[payer.lower()].remove_money(line[4])
        users[payee.lower()].add_money(line[4])
    except:
        fail(f"Support Bank.py. Could not confirm amount to float. Value: {line[4]}")

    return [users, transactions]


def read_data(filename):
    users = {}
    transactions = []

    if os.path.exists(filename) and len(filename.split(".")) > 1:
        parser = FileParser(filename)
        parser.parse()
        users = parser.getUsers()
        transactions = parser.getTransactions()

        if filename.split(".")[1] == "json":
            with open(filename) as json_file:
                data = json.load(json_file)
                for line_dict in data:
                    line = [line_dict['date'], line_dict['fromAccount'], line_dict['toAccount'], line_dict['narrative'], line_dict['amount']]
                    users, transactions = process_line(users, transactions, line)
            fail(f"Loaded file {filename} in JSON format")
        elif filename.split(".")[1] == "csv":
            with open(filename) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                headers = next(csv_reader)
                for line in csv_reader:
                    users, transactions = process_line(users, transactions, line)
            fail(f"Loaded file {filename} in CSV format")
        elif filename.split(".")[1] == "xml":
            tree = et.parse(filename)
            root = tree.getroot()
            line = []
            for child in root:
                date = child.attrib["Date"]
                narrative = child[0].text
                amount = child[1].text
                payer = child[2][0].text
                payee = child[2][1].text
                date = datetime(year=1900, month=12, day=31) + timedelta(days=int(date))
                date = date.strftime('%Y-%m-%d')
                line = [date, payer, payee, narrative, amount]
                users, transactions = process_line(users, transactions, line)
            fail(f"Loaded file {filename} in XML format")
        else:
            fail("This is not a valid file type")
    else:
        if os.path.exists(filename):
            fail("That file has no extension")
        else:
            fail("That file does not exist")
    return [users, transactions]


def verify_command(users):
    valid = False
    while not valid:
        print("╔═════════════════════════╦════════════════════════════════════════════════╗")
        print("║        COMMANDS         ║                     BY                         ║")
        print("║ 1. List ALL             ║    |---                                    ©   ║")
        print("║ 2. List <Account>       ║    |    | |   | |---|  |----  |---|  |---|     ║")
        print("║ 3. Import File <File>   ║    |    | |   | |   |  |      |---|  |   |     ║")
        print("║ 4. Exit                 ║    |----   ---  |   |  |----  |   |  |   |     ║")
        print("║ 5. ????                 ║                  (and ben)                     ║")
        print("╚═════════════════════════╩════════════════════════════════════════════════╝\n")

        answer = input("- Command: ")
        key = answer[5:].lower()

        if answer.lower() == "list all" or answer.lower() == "exit" or answer[:11].lower() == "import file":
            valid = True
        elif answer[:4].lower() == "list":
            if key in users:
                valid = True
            else:
                fail("This user does not exist")
        else:
            fail("That's not a command")

    return answer


def perform_command(users, transactions, command):
    if command.lower() == "exit":
        fail("User exited")
        pass
    elif command[:11].lower() == "import file":
        filename = command[12:]
        users, transactions = read_data(filename)
        return [users, transactions]
    elif command.lower() == "list all":
        if len(users) == 0:
            fail("There are no users loaded in")
        for key in users:
            print(f"{users[key].name} {'is owed' if users[key].balance > 0 else 'owes'} £{abs(users[key].balance):.2f}")
    else:
        key = command[5:].lower()
        print(f"{users[key].name} {'is owed' if users[key].balance > 0 else 'owes'} £{abs(users[key].balance):.2f}")

        for transaction in transactions:
            if transaction.payer.lower() == key or transaction.payee.lower() == key:
                print(
                    f"Transaction: £{transaction.amount} from {transaction.payer} to {transaction.payee} (Date {transaction.date}, Reason: {transaction.reason})")


def start():
    logging.basicConfig(filename="SupportBank.log", filemode="w", level=logging.DEBUG)

    users = {}
    transactions = []
    command = ""
    while not command == "exit":
        command = verify_command(users)
        output = perform_command(users, transactions, command)

        if output:
            users, transactions = output


start()

