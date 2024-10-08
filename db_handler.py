import pyodbc


def _prepare_table(cnxn: pyodbc.Connection) -> None:
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


def create_db_connection(db_driver: str, db_server: str, db_name: str, db_user: str, db_pass: str) -> pyodbc.Connection:
    db_driver = '{' + db_driver + '}'
    connection_string = f'DRIVER={db_driver};SERVER={db_server};DATABASE={db_name};UID={db_user};PWD={db_pass}'
    cnxn = pyodbc.connect(connection_string)
    _prepare_table(cnxn)

    return cnxn


def insert_data(cnxn: pyodbc.Connection, mem_info: dict) -> None:
    query = 'INSERT INTO memory_log (used, available) VALUES (?, ?)'

    cursor = cnxn.cursor()
    cursor.execute(query, [mem_info['used'], mem_info['available']])
    cnxn.commit()
