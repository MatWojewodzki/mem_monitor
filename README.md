# mem_monitor
A simple Python script that monitors current RAM usage and writes the results to an SQL database in Azure.

## Requirements
- Python >=3.8
- ODBC driver

## Setting up
Provide environmental variables directly to your environment or create a .env file in the same directory. The names for the variables are:
- `DB_DRIVER` - ODBC driver name (eg. `'ODBC Driver 18 for SQL Server'`),
- `DB_SERVER`, `DB_NAME`, `DB_USER`, `DB_PASS` - your server credentials,
- `SAMPLING_INTERVAL` \[optional\] - the interval at which you want the program to check the memory status and write it to the database.

## License
mem_monitor is licensed under the MIT license. Check out LICENSE.txt for the full text.