# NHL-Database

This repository contains all the python and MySQL code to construct an automated NHL Fantasy Database.  All the code is geared to work off of the NHL's undocumented API.  For more information on the API please see: https://github.com/dword4/nhlapi.  To be succinct, this repository contains the code to construct an fully automated Fantasy Database.  It currently contains models to:
    * Asses a players impact on goal scoring (Uses a variation of the deep reinforcement learning model developed by Oliver Schulte and Guiland Liu).
    * Predicts the winner of a game.
In the future, I will be implementing an agent to automate Draft Kings Daily NHL Fantasy Competitions.  This will include:
  * Models to predict the number of goals, assists, hits, shots etc a player will score in a game.
  * An optimzation model to optimzation player select in Draft Kings Fantasy Competitions.
  * An agent to automate the entire process.
However, this won't be completed in the very near future simply because the NHL is currently in its off season and thus Draft Kings has no competitions. My estimated time to completion for this is approximately end of Dec 2021.

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
   * The first time this is executed, this code take well over a day to download all the data.  My recommendation to speed this up as model as possible is to adjust the functions that are called to write all the output into a csv file and then to dumpy the results into the corresponding table one at a time.  Note, be sure to follow the order set out in "daily_update.py".
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

#### weekly_update.py
This python script executes the weekly functinos required to keep the database up to date.  This includes:
  * Updating player attributes.
  * Creating a new backup of the server.
  * Uploading the new backup.
  * Deleting the old backup.

### Analysis/
#### Papers
This just contains some interesting and applicable papers.

#### player-valuation-deep_rl.ipynb

This jupyter notebook contains the development of the deep reinforcement learning model used to develop the GIM values that are used to determine a players impact on goal scoring.  This model and its content is a variation of the week done in "Deep Reinforcement Learning in Ice Hockey for Context-Aware Player Evaluation" by Oliver Schulte and Guiland Liu.

####  player-valuation_mdp.ipynb

This jupyter notebook contains the developement of a markov decision model used to develop the GIM values that are used to determine a players impact on goal scoring.  This model and its content is a variation of the week done in "A Markov Game Model for Valuing Player Actions in Ice Hockey" by Olver Schulte and Kurt Routley.

#### predicting_wins.ipynb

This jupyter notebook contains the development of the model used to determine the winner of a given game.

### DataGenerators

#### backup_generator.py
This script generates the back up of the SQL Server.  

NOTE: This script will be updated shortly to not use Google Drive.

#### boxscore_generator.py

This script pulls the boxscores for games.

#### conference_generator.py

This script pulls the conferences.

#### create_calendars.py

This script creates the schedule of the weekly and daily updates.

#### data_to_production.py

This script executes the store_procedures to move the data to the production database.

#### divisions_generator.py

This script pulls the divisions.

#### drafts_generator.py

This script pulls the drafts.

#### franchise_generator.py

This script pulls the franchises.

#### get_time.py

This script creates the current time in the required format.

#### live_data_generator.py

This script pulls the play-by-play data for games.

#### players_generator.py

This script pulls players and also contains all the functions to pull their attributes as well.

#### schedule_updator.py

This script pulls the schedule.

#### script_execution.py

This script contains the function used to recored the execution of scripts.

#### seasons_generator.py

This script pulls the seasons.

#### team_logo_generator.py

This script pulls the team logos.

#### teams_generator.py

This script pulls the teams.

#### trohpy_generator.py

This script pulls the trohpies.

#### trophy_winner_generator.py

This script pulls the trophy winners.
