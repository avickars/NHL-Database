# NHL-Database

This repository contains all the python and MySQL code to construct an automated NHL Fantasy Database.

## Configuring the DataBase and Automation

### Steps

1. Configure a MySQL Server:
   * Create an initial database called "hockey"
   * Alter the credentials in "SQLCode/DatabaseCredentials.py"
2. Configure a python environment.  You will need the following packages:
   * Numpy
   * Pandas
   * Skikit-learn
   * Pickle
   * PyTorch
   * MySQL-Connector
   * All other packages are default python packages and should not need to be installed.
4. Execute create all tables and databases defined in "SQLCode/tables.sql".
5. Created all stored procedures in "SQLCode/stored_procedures".
6. Execute "yearly_update.py"
7. Execute "daily_update.py"

