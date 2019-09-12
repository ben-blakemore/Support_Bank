from User import User
from Transactions import Transactions
from datetime import datetime
from datetime import timedelta
import xml.etree.ElementTree as et
import csv
import json


class FileParser():
    def __init__(self, logger, filename):
        file_split = filename.split('.')

        self.filename = filename
        self.file = ".".join(file_split[:len(file_split) - 1])
        self.extension = file_split[len(file_split) - 1]
        self.users = {}
        self.transactions = []
        self.logger = logger

    def parse_json(self):
        with open(self.filename) as json_file:
            data = json.load(json_file)
            for line_dict in data:
                line = [line_dict['date'], line_dict['fromAccount'], line_dict['toAccount'], line_dict['narrative'], line_dict['amount']]
                self.process_line(line)

        self.logger.fail(f"Loaded file {self.filename} in JSON format")

    def parse_csv(self):
        with open(self.filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            headers = next(csv_reader)
            for line in csv_reader:
                self.process_line(line)

        self.logger.fail(f"Loaded file {self.filename} in CSV format")

    def parse_xml(self):
        tree = et.parse(self.filename)
        root = tree.getroot()
        line = []
        for child in root:
            date = child.attrib["Date"]
            narrative = child[0].text
            amount = child[1].text
            payer = child[2][0].text
            payee = child[2][1].text
            date = datetime(year=1900, month=1, day=1) + timedelta(days=int(date))
            date = date.strftime('%Y-%m-%d')
            line = [date, payer, payee, narrative, amount]
            self.process_line(line)


        self.logger.fail(f"Loaded file {self.filename} in XML format")

    def parse(self):
        if self.filename.split(".")[1] == "json":
            self.parse_json()
        elif self.filename.split(".")[1] == "csv":
            self.parse_csv()
        elif self.filename.split(".")[1] == "xml":
            self.parse_xml()
        else:
            self.logger.fail("This is not a valid file type")

    def process_line(self, line):
        payer = line[1]
        payee = line[2]

        if payer.lower() not in self.users:
            self.users[payer.lower()] = User(payer)
        if payee.lower() not in self.users:
            self.users[payee.lower()] = User(payee)
        try:
            self.transactions.append(Transactions(line))
            self.users[payer.lower()].remove_money(line[4])
            self.users[payee.lower()].add_money(line[4])
        except:
            self.logger.fail(f"Support Bank.py. Could not confirm amount to float. Value: {line[4]}")

    def get_users(self):
        return self.users

    def get_transactions(self):
        return self.transactions
