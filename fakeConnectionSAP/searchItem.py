import json
import sqlite3
from fakeConnectionSAP.constants import FIELD_ID, ITEM_TABLE_NAME


def search_item(id_item, db_uri) -> list:
    """
    Search an item in the DB by its id and returns a list of the assembly lines that this item should go.

    Args:
        id_item (str): The id of the item
        db_uri (str): The uri where the DB is located.
    """

    lines = None

    connection = sqlite3.connect(db_uri)
    cursor = connection.cursor()

    cursor.execute(f"select * from {ITEM_TABLE_NAME} where {FIELD_ID}=:d", {"d": id_item})
    search_result = cursor.fetchall()

    if search_result:
        lines = json.loads(search_result[0][1])

    connection.commit()
    connection.close()

    return lines
