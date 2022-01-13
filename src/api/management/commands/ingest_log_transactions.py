from datetime import datetime
from django.core.management.base import BaseCommand
import json

from api.controllers.create_transaction import CreateTransactionController
from api.controllers.delete_all_transactions import DeleteAllTransactionsController

class Command(BaseCommand):
    help = 'Transfers log data from the old storage format (log.txt file) into the TransactionHistoryStore table'

    def handle(self, *args, **options):
        num_deleted = DeleteAllTransactionsController().process()
        counter = 0
        num_inserted = 0
        # Transaction Histories used to be stored in a giant log file. Ingest that log file into the db
        with open("../static_sources/data.log", "r") as log:
            for line in log:
                try:
                    data = json.loads(line)
                    timestamp = datetime.strptime(data['TIMESTAMP'], '%Y-%m-%d %I:%M:%S %p')
                    if counter % 100 == 1:
                        print(timestamp)
                    if timestamp.year == 2021 and timestamp.month > 7:
                        counter += 1
                        inserted = CreateTransactionController(data).process()
                        num_inserted += inserted
                except Exception as e:
                    pass
        print("{} Entries Deleted".format(num_deleted))
        print("{} Entries Inserted".format(num_inserted))