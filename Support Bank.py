import os
from FileParser import FileParser
from Logger import Logger
from FileExport import FileExport


def read_data(logger, filename):
    users = {}
    transactions = []

    if os.path.exists(filename) and len(filename.split(".")) > 1:
        parser = FileParser(logger, filename)
        parser.parse()
        users = parser.get_users()
        transactions = parser.get_transactions()
    else:
        if os.path.exists(filename):
            logger.fail("That file has no extension")
        else:
            logger.fail("That file does not exist")
    return [users, transactions]


def verify_command(logger, users):
    valid = False
    while not valid:
        print("╔═════════════════════════╦════════════════════════════════════════════════╗")
        print("║        COMMANDS         ║                     BY                         ║")
        print("║ 1. Import File <File>   ║    |---                                    ©   ║")
        print("║ 2. Export File <File>   ║    |    | |   | |---|  |----  |---|  |---|     ║")
        print("║ 3. List ALL             ║    |    | |   | |   |  |      |   |  |   |     ║")
        print("║ 4. List <Account>       ║    |    | |   | |   |  |      |---|  |   |     ║")
        print("║ 5. Exit                 ║    |----   ---  |   |  |----  |   |  |   |     ║")
        print("║ 6. ????                 ║                  (and ben)                     ║")
        print("╚═════════════════════════╩════════════════════════════════════════════════╝\n")

        answer = input("- Command: ")
        key = answer[5:].lower()

        if answer.lower() in ["list all", "exit", "????"] or answer[:11].lower() in ["import file", "export file"]:
            valid = True
        elif answer[:4].lower() == "list":
            if key in users:
                valid = True
            else:
                logger.fail("This user does not exist")
        else:
            logger.fail("That's not a command")

    return answer


def process_export(logger, filename, transactions):
    file_split = filename.split(".")
    extension = file_split[len(file_split) - 1]

    exporter = FileExport(logger)

    if extension == "csv":
        exporter.export_csv(filename, transactions)
    elif extension == "json":
        exporter.export_json(filename, transactions)
    elif extension == "xml":
        exporter.export_xml(filename, transactions)


def perform_command(logger, users, transactions, command):
    if command.lower() == "exit":
        logger.fail("User exited")
        exit(0)
    elif command.lower() == "????":
        aardvark()
        input("Press enter to continue")
    elif command[:11].lower() == "import file":
        filename = f"transactions/{command[12:]}"
        users, transactions = read_data(logger, filename)
        input("Press enter to continue")
        return [users, transactions]
    elif command[:11].lower() == "export file":
        filename = f"transactions/{command[12:]}"
        process_export(logger, filename, transactions)
    elif command.lower() == "list all":
        if len(users) == 0:
            logger.fail("There are no users loaded in")
        else:
            logger.fail("User printed list of accounts")
            for key in users:
                print(f"{users[key].name} {'is owed' if users[key].balance > 0 else 'owes'} £{abs(users[key].balance):.2f}")
        input("Press enter to continue")
    else:
        key = command[5:].lower()
        logger.fail(f"User printed list of transactions involving {users[key].name}")
        print(f"{users[key].name} {'is owed' if users[key].balance > 0 else 'owes'} £{abs(users[key].balance):.2f}")
        for transaction in transactions:
            if transaction.payer.lower() == key or transaction.payee.lower() == key:
                print(f"Transaction: £{transaction.amount} from {transaction.payer} to {transaction.payee} (Date {transaction.date}, Reason: {transaction.reason})")
        input("Press enter to continue")

def aardvark():
    print("Aaron Aardvark says Hello!")
    print("              _. - --._  /\ ")
    print("         ./ '       ''--`\//")
    print("        ./               o  \\")
    print("        /./ \  )______   \__ \\")
    print("      . / / /\ \   | \ \     \\ \\")
    print("        / /   \ \  | | \ \    \\ 7")
    print("        ''     ''   ''  ''        ")


def start():
    logger = Logger()
    users = {}
    transactions = []

    while True:
        command = verify_command(logger, users)
        output = perform_command(logger, users, transactions, command)

        if output:
            users, transactions = output


start()

