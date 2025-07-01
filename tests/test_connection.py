from config.db import get_transactions_collection

collection = get_transactions_collection()
sample= collection.find_one()
print(sample)
