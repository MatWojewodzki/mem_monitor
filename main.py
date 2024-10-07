import os
import time
from pyodbc import Error as DBError
from dotenv import load_dotenv
import memory
import db_handler


INTERVAL_ENV = 'SAMPLING_INTERVAL'
DRIVER_ENV = 'DB_DRIVER'
SERVER_ENV = 'DB_SERVER'
DATABASE_ENV = 'DB_NAME'
USERNAME_ENV = 'DB_USER'
PASSWORD_ENV = 'DB_PASS'

DEFAULT_SAMPLING_INTERVAL = 5


def current_time_log():
    return time.strftime('%H:%M:%S', time.gmtime())


def monitor(db_driver, db_server, db_name, db_user, db_pass):
    cnxn = db_handler.create_db_connection(db_driver, db_server, db_name, db_user, db_pass)
    last_time = time.perf_counter()
    while True:
        memory_info = memory.get_memory_info()
        print(f'[MEM_LOG][{current_time_log()}] {memory_info}')
        db_handler.insert_data(cnxn, memory_info)
        desired_dt = os.getenv(INTERVAL_ENV, DEFAULT_SAMPLING_INTERVAL)
        time.sleep(desired_dt - (time.perf_counter() - last_time))
        last_time = time.perf_counter()


def main():
    load_dotenv()

    db_driver = os.getenv(DRIVER_ENV)
    db_server = os.getenv(SERVER_ENV)
    db_name = os.getenv(DATABASE_ENV)
    db_user = os.getenv(USERNAME_ENV)
    db_pass = os.getenv(PASSWORD_ENV)

    try:
        monitor(db_driver, db_server, db_name, db_user, db_pass)
    except KeyboardInterrupt:
        print('KeybordInterrupt')
    except DBError as e:
        print(f'A Database Error Occured: {e}')
    finally:
        print('Closing application.')


if __name__ == '__main__':
    main()
