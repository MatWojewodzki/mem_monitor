import os
import pyodbc

DRIVER = '{ODBC Driver 18 for SQL Server}'

SERVER_ENV = 'DB_SERVER'
DATABASE_ENV = 'DB_NAME'
USERNAME_ENV = 'DB_USER'
PASSWORD_ENV = 'DB_PASS'


def _prepare_table(cnxn):
    delete_query = 'DROP TABLE IF EXISTS memory_log'
    create_query = '''
        CREATE TABLE memory_log (
            log_id INT NOT NULL IDENTITY(1, 1),
            used VARCHAR(8),
            available VARCHAR(8),
            time DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (log_id)
        )
    '''
    cursor = cnxn.cursor()
    cursor.execute(delete_query)
    cursor.execute(create_query)
    cnxn.commit()


def create_db_connection():
    server = os.getenv(SERVER_ENV)
    db_name = os.getenv(DATABASE_ENV)
    db_user = os.getenv(USERNAME_ENV)
    db_pass = os.getenv(PASSWORD_ENV)

    connection_string = f'DRIVER={DRIVER};SERVER={server};DATABASE={db_name};UID={db_user};PWD={db_pass}'
    cnxn = pyodbc.connect(connection_string)
    _prepare_table(cnxn)

    return cnxn


def insert_data(cnxn, mem_info):
    query = 'INSERT INTO memory_log (used, available) VALUES (?, ?)'

    cursor = cnxn.cursor()
    cursor.execute(query, [mem_info['used'], mem_info['available']])
    cnxn.commit()
