from datasette import hookimpl
import sqlite3
import sys

CONSTANTS = {
    getattr(sqlite3, constant): constant
    for constant in dir(sqlite3)
    if constant
    in (
        "SQLITE_ALTER_TABLE",
        "SQLITE_ANALYZE",
        "SQLITE_ATTACH",
        "SQLITE_CREATE_INDEX",
        "SQLITE_CREATE_TABLE",
        "SQLITE_CREATE_TEMP_INDEX",
        "SQLITE_CREATE_TEMP_TABLE",
        "SQLITE_CREATE_TEMP_TRIGGER",
        "SQLITE_CREATE_TEMP_VIEW",
        "SQLITE_CREATE_TRIGGER",
        "SQLITE_CREATE_VIEW",
        "SQLITE_CREATE_VTABLE",
        "SQLITE_DELETE",
        "SQLITE_DENY",
        "SQLITE_DETACH",
        "SQLITE_DONE",
        "SQLITE_DROP_INDEX",
        "SQLITE_DROP_TABLE",
        "SQLITE_DROP_TEMP_INDEX",
        "SQLITE_DROP_TEMP_TABLE",
        "SQLITE_DROP_TEMP_TRIGGER",
        "SQLITE_DROP_TEMP_VIEW",
        "SQLITE_DROP_TRIGGER",
        "SQLITE_DROP_VIEW",
        "SQLITE_DROP_VTABLE",
        "SQLITE_FUNCTION",
        "SQLITE_IGNORE",
        "SQLITE_INSERT",
        "SQLITE_OK",
        "SQLITE_PRAGMA",
        "SQLITE_READ",
        "SQLITE_RECURSIVE",
        "SQLITE_REINDEX",
        "SQLITE_SAVEPOINT",
        "SQLITE_SELECT",
        "SQLITE_TRANSACTION",
        "SQLITE_UPDATE",
    )
}


def print_authorizer(action, table, column, db_name, trigger_name):
    bits = ["{}: ".format(CONSTANTS.get(action, action))]
    if table:
        bits.append('table="{}"'.format(table))
    if column:
        bits.append('column="{}"'.format(column))
    if db_name:
        bits.append("db_name={}".format(db_name))
    if trigger_name:
        bits.append('trigger_name="{}"'.format(trigger_name))
    print(" ".join(bits), file=sys.stderr)
    return sqlite3.SQLITE_OK


@hookimpl
def prepare_connection(conn):
    conn.set_authorizer(print_authorizer)
