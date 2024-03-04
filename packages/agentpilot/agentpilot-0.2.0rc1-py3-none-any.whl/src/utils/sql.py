import asyncio
import os.path
import sqlite3
import sys
import threading

from packaging import version

from src.gui.components.config import ConfigTree

sql_thread_lock = threading.Lock()


def get_db_path():
    from src.utils.filesystem import get_application_path
    # Check if we're running as a script or a frozen exe
    if getattr(sys, 'frozen', False):
        application_path = get_application_path()
    else:
        application_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))

    ret = os.path.join(application_path, 'data.db')
    return ret


def execute(query, params=None):
    with sql_thread_lock:
        # Connect to the database
        db_path = get_db_path()
        with sqlite3.connect(db_path) as conn:
            # Create a cursor object
            cursor = conn.cursor()

            # Execute the query
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Commit the changes
            # conn.commit()

            # Close the cursor and connection
            cursor.close()
            # conn.close()
            return cursor.lastrowid


def get_results(query, params=None, return_type='rows', incl_column_names=False):
    # Connect to the database
    db_path = get_db_path()
    with sqlite3.connect(db_path) as conn:
        # Create a cursor object
        cursor = conn.cursor()

        # Execute the query
        if params:
            # make new tuple and replace where isinstance configtreewidget
            param_list = []
            for p in params:
                if isinstance(p, ConfigTree):
                    item = p.tree.currentItem()
                    if item:
                        param_list.append(item.text(1))
                else:
                    param_list.append(p)
            cursor.execute(query, param_list)
        else:
            cursor.execute(query)

        # Fetch all the rows as a list of tuples
        rows = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        # conn.close()

    col_names = [description[0] for description in cursor.description]

    # Return the rows
    if return_type == 'list':
        ret_val = [row[0] for row in rows]
    elif return_type == 'dict':
        ret_val = {row[0]: row[1] for row in rows}
    elif return_type == 'hdict':
        # use col names as keys and first row as values
        if len(rows) == 0:
            return None
        ret_val = {col_names[i]: rows[0][i] for i in range(len(col_names))}
    elif return_type == 'htuple':
        if len(rows) == 0:
            return None
        ret_val = rows[0]
    else:
        ret_val = rows

    if incl_column_names:
        return ret_val, col_names
    else:
        return ret_val


def get_scalar(query, params=None):
    # Connect to the database
    db_path = get_db_path()
    with sqlite3.connect(db_path) as conn:
        # Create a cursor object
        cursor = conn.cursor()

        # Execute the query
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # Fetch the first row
        row = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        # conn.close()

        if row is None:
            return None
        return row[0]


def check_database_upgrade():
    db_path = get_db_path()
    file_exists = os.path.isfile(db_path)
    if not file_exists:
        raise Exception('NO_DB')

    db_version_str = get_scalar("SELECT value as app_version FROM settings WHERE field = 'app_version'")
    db_version = version.parse(db_version_str)
    app_version = version.parse('0.1.0')
    if db_version > app_version:
        raise Exception('OUTDATED_APP')
    elif db_version < app_version:
        return db_version
    else:
        return None


def execute_multiple(queries, params_list):
    with sql_thread_lock:
        # Connect to the database
        db_path = get_db_path()
        with sqlite3.connect(db_path) as conn:
            # try:
                # Create a cursor object
            cursor = conn.cursor()

            try:
                for query, params in zip(queries, params_list):
                    cursor.execute(query, params)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise
            finally:
                cursor.close()
