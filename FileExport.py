import csv
import json
import xml.etree.ElementTree as et
from xml.dom import minidom
from datetime import datetime
from datetime import date


class FileExport:
    def __init__(self, logger):
        self.logger = logger

    def export_csv(self, filename, transactions):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "From", "To", "Narrative", "Amount"])

            for transaction in transactions:
                line = [transaction.date, transaction.payer, transaction.payee, transaction.reason, transaction.amount]
                writer.writerow(line)

        self.logger.fail(f"Exported file to {filename} in CSV format")

    def create_xml_child(self, parent, name, text =""):
        child = et.Element(name)
        child.text = text
        parent.append(child)

        return child

    def export_xml(self, filename, transactions):
        root = et.Element("TransactionList")

        date1 = date(1900, 1, 1)

        for transaction in transactions:
            date2 = datetime.strptime(transaction.date, "%Y-%m-%d").date()
            days_between = (date2-date1).days
            child_1 = self.create_xml_child(root, "SupportTransaction")
            child_1.attrib = {"Date" : str(days_between)}
            self.create_xml_child(child_1, "Description", transaction.reason)
            self.create_xml_child(child_1, "Value", str(transaction.amount))
            child_4 = self.create_xml_child(child_1, "Parties")
            self.create_xml_child(child_4, "From", transaction.payer)
            self.create_xml_child(child_4, "To", transaction.payee)

        xlmstr = minidom.parseString(et.tostring(root)).toprettyxml(indent="  ")
        with open(filename, "w") as f:
            f.write(xlmstr)

        self.logger.fail(f"Exported file to {filename} in XML format")

    def export_json(self, filename, transactions):
        with open(filename, 'w', newline='') as f:
            export_data = []
            for transaction in transactions:
                line = {"date":transaction.date, "fromAccount":transaction.payer, "toAccount":transaction.payee, "narrative":transaction.reason, "amount":transaction.amount}
                export_data.append(line)
            f.write(json.dumps(export_data, indent=2))

        self.logger.fail(f"Exported file to {filename} in JSON format")