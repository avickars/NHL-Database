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

## Detailed Description of Each File

#### daily_update.py
This python script executes the daily functions required to keep the database up to date.  This includes:
  * Getting the schedule of games up to the current date.  Note, It does pull any scheduled games past the current date.  This is to allow for any games that get rescheduled.
  * Getting the play-by-play data for new games.
  * Getting the boxscore data for any new games.
  * Getting any new players.
  * Create the Sequences of events that are used in the GIM model.
  * Feeds the sequences created in the above step into the GIM model.
  * Consolidates the GIMs created in the above step.
  * Formats the for the game outcome predictor model.
  * Predicts the game outcomes for future games.
  * Moves the data to the production database for the PowerBI Report to pick up.

#### yearly_update.py
This python script executes the yearly functions required to keep the database up to date.  This includes:
  * Updating the historical GIM values.  These are used in the consolidation of the GIM values in the daily update.
  * Updates the conferences.
  * Updates the divisions.
  * Updates the franchises.
  * Updates the teams.
  * Updates the seasons.
  * Updates the drafts.
  * Updates the prospects.
  * Updates the trophy winners.
  * Updates the logos.

