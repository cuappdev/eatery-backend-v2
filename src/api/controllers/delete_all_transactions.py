
from api.models import TransactionHistoryStore

class DeleteAllTransactionsController:

    def process(self):
        return TransactionHistoryStore.objects.all().delete()[0]
        