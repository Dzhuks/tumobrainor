from src.constants import DB_PATH
from src.data_store import CSVDataStore

csv = CSVDataStore(DB_PATH)
print(csv.get_stat())
