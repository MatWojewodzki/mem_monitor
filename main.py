import os
import time
from pyodbc import Error as DBError
from dotenv import load_dotenv
import memory
import db_handler


INTERVAL_ENV = 'SAMPLING_INTERVAL'
DEFAULT_SAMPLING_INTERVAL = 5


def current_time_log():
    return time.strftime('%H:%M:%S', time.gmtime())


def monitor():
    cnxn = db_handler.create_db_connection()
    last_time = time.perf_counter()
    while True:
        memory_info = memory.get_memory_info()
        print(f'[MEM_LOG][{current_time_log()}] {memory_info}')
        db_handler.insert_data(cnxn, memory_info)
        desired_dt = os.getenv(INTERVAL_ENV, DEFAULT_SAMPLING_INTERVAL)
        time.sleep(desired_dt - (time.perf_counter() - last_time))
        last_time = time.perf_counter()


def main():
    load_dotenv(override=True)
    try:
        monitor()
    except KeyboardInterrupt:
        print('KeybordInterrupt')
    except DBError as e:
        print(f'A Database Error Occured: {e}')
    finally:
        print('Closing application.')


if __name__ == '__main__':
    main()
