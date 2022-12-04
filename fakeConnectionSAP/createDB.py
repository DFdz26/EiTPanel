import sqlite3
import json
from fakeConnectionSAP.constants import FIELD_ID, FIELD_LINES, ITEM_TABLE_NAME, DB_NAME


def createFakeDB(verbose=True):
    """
    Before using this function, make sure to not have created the file 'items.db' before. In case of so, please
    delete it. Since I'm using the absolute path of the DB file, I can't check if the file already exists without
    administrative permissions.
    """

    items = [
        {"Id": "4465441", "Lines": [3]},
        {"Id": "602173", "Lines": [1]},
        {"Id": "4320058", "Lines": [3]},
        {"Id": "9320058", "Lines": [1, 2]},
    ]

    stored_items = []

    for item in items:
        id_item = item["Id"]
        lines = json.dumps(item["Lines"])
        stored_items.append((id_item, lines))

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(f"CREATE TABLE IF NOT EXISTS {ITEM_TABLE_NAME} ({FIELD_ID} text, {FIELD_LINES} text)")
    cursor.executemany(f"insert into {ITEM_TABLE_NAME} values (?, ?)", stored_items)

    # print the database
    if verbose:
        for row in cursor.execute(f"select * from {ITEM_TABLE_NAME}"):
            print(row)

    connection.commit()
    connection.close()


if __name__ == '__main__':
    createFakeDB()
