import csv
import os
from datetime import date
from pathlib import Path

import pandas as pd
from src.constants import BRAIN_TUMOR_TYPES, DB_FIELDNAMES


class AbstractDataStore:
    def get_labels(self) -> list:
        raise NotImplementedError

    def add_record(self, record: dict) -> None:
        raise NotImplementedError

    def remove_record(self, record_id: int) -> None:
        raise NotImplementedError

    def get_records_number(self) -> int:
        raise NotImplementedError

    def get_records(self, records_number: int) -> list[dict]:
        raise NotImplementedError

    def get_record(self, record_id: int) -> dict:
        raise NotImplementedError

    def get_stat(self, records_number: int) -> list[dict]:
        raise NotImplementedError


class CSVDataStore(AbstractDataStore):
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self._create_db_if_not_exist()
        self.df = pd.read_csv(self.db_path, delimiter=";")

    def _create_db_if_not_exist(self):
        if os.path.isfile(self.db_path):
            return
        with open(self.db_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, delimiter=";", fieldnames=DB_FIELDNAMES, lineterminator="\n")
            writer.writeheader()

    def get_labels(self) -> list:
        return self.df.columns.tolist()

    def add_record(self, record: dict) -> None:
        with open(self.db_path, "a+", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, delimiter=";", fieldnames=DB_FIELDNAMES, lineterminator="\n")
            di = {
                DB_FIELDNAMES[0]: date.today().strftime("%d/%m/%Y"),
                DB_FIELDNAMES[1]: record["filename"],
                DB_FIELDNAMES[2]: record["brain_tumor_type"],
            }
            writer.writerow(di)
        self.df = pd.read_csv(self.db_path, delimiter=";")

    def get_records_number(self) -> int:
        return len(self.df)

    def get_records(self, records_number: int) -> list[list]:
        with open(self.db_path, newline="", encoding="utf-8") as csvfile:
            rows = [line.strip().split(";") for line in csvfile.readlines()[1:][-records_number:]]
            return rows

    def get_stat(self, records_number: int) -> list[dict]:
        stat = []
        brain_tumor_type_col = DB_FIELDNAMES[DB_FIELDNAMES.index("Тип опухоли")]
        dr_range = self.df.tail(records_number)
        for brain_tumor_type in BRAIN_TUMOR_TYPES:
            di = {}
            di["title"] = brain_tumor_type
            columns = (
                dr_range[dr_range[brain_tumor_type_col] == brain_tumor_type][brain_tumor_type_col]
                .value_counts()
                .to_list()
            )
            if columns:
                di["value"] = columns[0]
            else:
                di["value"] = 0
            di["percent"] = int(round(di["value"] / records_number * 100))
            stat.append(di)
        return stat
