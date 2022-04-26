import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
from DataGenerators.get_time import get_time
import pandas as pd
import numpy as np
import datetime
from DataGenerators.players_generator import *
from mysql.connector.errors import Error
from datetime import date


def main():
	# Opening connection
	creds = DBC.DataBaseCredentials()
	conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
	connection = conn.open()
	cursor = connection.cursor()

	# Getting all the games we need to get the live data for (i.e. everything from our last run up to games played yesterday)
	games = pd.read_sql_query("select gameID from schedules where seasonID=20212022 and gameType=\'R\'", connection)

	goalies = []

	skaters = []

	for index, gameID in games.iterrows():
		print(gameID)
		gameID = gameID.values[0]

		url_string = f"https://statsapi.web.nhl.com/api/v1/game/{gameID}/feed/live"
		url = requests.get(url_string)
		url_data = url.json()

		# Getting player Stats
		for team in ['away', 'home']:
			try:
				teamID = url_data['liveData']['boxscore']['teams'][team]['team']['id']
			except KeyError:
				teamID = 'NULL'

			# Getting players who played
			players = url_data['liveData']['boxscore']['teams'][team]['players']

			for player in players:
				playerID = players[player]['person']['id']

				playerName = players[player]['person']['fullName']

				if players[player]['position']['code'] == 'G':
					try:
						stats = players[player]['stats']['goalieStats']
					except KeyError:
						continue

					# ******************

					try:
						timeOnIce = stats['timeOnIce']
					except KeyError:
						timeOnIce = None

					try:
						assists = stats['assists']
					except KeyError:
						assists = None

					try:
						goals = stats['goals']
					except KeyError:
						goals = None

					try:
						pim = stats['pim']
					except KeyError:
						pim = None

					try:
						shots = stats['shots']
					except KeyError:
						shots = None

					# ******************

					try:
						saves = stats['saves']
					except KeyError:
						saves = None

					try:
						powerPlaySaves = stats['powerPlaySaves']
					except KeyError:
						powerPlaySaves = None

					try:
						shortHandedSaves = stats['shortHandedSaves']
					except KeyError:
						shortHandedSaves = None

					try:
						evenSaves = stats['evenSaves']
					except KeyError:
						evenSaves = None

					try:
						shortHandedShotsAgainst = stats['shortHandedShotsAgainst']
					except KeyError:
						shortHandedShotsAgainst = None

					try:
						evenShotsAgainst = stats['evenShotsAgainst']
					except KeyError:
						evenShotsAgainst = None

					# ******************

					try:
						powerPlayShotsAgainst = stats['powerPlayShotsAgainst']
					except KeyError:
						powerPlayShotsAgainst = None

					try:
						decision = stats['decision']
					except KeyError:
						decision = None

					try:
						savePercentage = stats['savePercentage']
					except KeyError:
						savePercentage = None

					try:
						evenStrengthSavePercentage = stats['evenStrengthSavePercentage']
					except KeyError:
						evenStrengthSavePercentage = None

					try:
						powerPlaySavePercentage = stats['powerPlaySavePercentage']
					except KeyError:
						powerPlaySavePercentage = None

					goalies.append([gameID,
									teamID,
									playerID,
									playerName,
									timeOnIce,
									assists,
									goals,
									pim,
									shots,
									saves,
									powerPlaySaves,
									shortHandedSaves,
									evenSaves,
									shortHandedShotsAgainst,
									evenShotsAgainst,
									powerPlayShotsAgainst,
									decision,
									savePercentage,
									evenStrengthSavePercentage,
									powerPlaySavePercentage])

				else:
					try:
						stats = players[player]['stats']['skaterStats']
					except KeyError:
						continue

					# ******************

					try:
						timeOnIce = stats['timeOnIce']
					except KeyError:
						timeOnIce = None

					try:
						assists = stats['assists']
					except KeyError:
						assists = None

					try:
						goals = stats['goals']
					except KeyError:
						goals = None

					try:
						shots = stats['shots']
					except KeyError:
						shots = None

					try:
						hits = stats['hits']
					except KeyError:
						hits = None

					# ******************

					try:
						powerPlayGoals = stats['powerPlayGoals']
					except KeyError:
						powerPlayGoals = None

					try:
						powerPlayAssists = stats['powerPlayAssists']
					except KeyError:
						powerPlayAssists = None

					try:
						penaltyMinutes = stats['penaltyMinutes']
					except KeyError:
						penaltyMinutes = None

					try:
						faceOffPct = stats['faceOffPct']
					except KeyError:
						faceOffPct = None

					try:
						faceOffWins = stats['faceOffWins']
					except KeyError:
						faceOffWins = None

					# ******************
					try:
						faceoffTaken = stats['faceoffTaken']
					except KeyError:
						faceoffTaken = None

					try:
						takeaways = stats['takeaways']
					except KeyError:
						takeaways = None

					try:
						giveaways = stats['giveaways']
					except KeyError:
						giveaways = None

					try:
						shortHandedGoals = stats['shortHandedGoals']
					except KeyError:
						shortHandedGoals = None

					try:
						shortHandedAssists = stats['shortHandedAssists']
					except KeyError:
						shortHandedAssists = None

					# ******************

					try:
						blocked = stats['blocked']
					except KeyError:
						blocked = None

					try:
						plusMinus = stats['plusMinus']
					except KeyError:
						plusMinus = None

					try:
						evenTimeOnIce = stats['evenTimeOnIce']
					except KeyError:
						evenTimeOnIce = None

					try:
						powerPlayTimeOnIce = stats['powerPlayTimeOnIce']
					except KeyError:
						powerPlayTimeOnIce = None

					try:
						shortHandedTimeOnIce = stats['shortHandedTimeOnIce']
					except KeyError:
						shortHandedTimeOnIce = None

					skaters.append([gameID,
									teamID,
									playerID,
									playerName,
									timeOnIce,
									assists,
									goals,
									shots,
									hits,
									powerPlayGoals,
									powerPlayAssists,
									penaltyMinutes,
									faceOffPct,
									faceOffWins,
									faceoffTaken,
									takeaways,
									giveaways,
									shortHandedGoals,
									shortHandedAssists,
									blocked,
									plusMinus,
									evenTimeOnIce,
									powerPlayTimeOnIce,
									shortHandedTimeOnIce])

	goalies = pd.DataFrame(goalies, columns=['gameID',
											 'teamID',
											 'playerID',
											 'playerName',
											 'timeOnIce',
											 'assists',
											 'goals',
											 'pim',
											 'shots',
											 'saves',
											 'powerPlaySaves',
											 'shortHandedSaves',
											 'evenSaves',
											 'shortHandedShotsAgainst',
											 'evenShotsAgainst',
											 'powerPlayShotsAgainst',
											 'decision',
											 'savePercentage',
											 'evenStrengthSavePercentage',
											 'powerPlaySavePercentage'])

	goalies.to_csv('data/goalies_boxscores.csv')

	skaters = pd.DataFrame(skaters,
						   columns=['gameID',
									'teamID',
									'playerID',
									'playerName',
									'timeOnIce',
									'assists',
									'goals',
									'shots',
									'hits',
									'powerPlayGoals',
									'powerPlayAssists',
									'penaltyMinutes',
									'faceOffPct',
									'faceOffWins',
									'faceoffTaken',
									'takeaways',
									'giveaways',
									'shortHandedGoals',
									'shortHandedAssists',
									'blocked',
									'plusMinus',
									'evenTimeOnIce',
									'powerPlayTimeOnIce',
									'shortHandedTimeOnIce'])

	skaters.to_csv('data/skaters_boxscores.csv')

	conn.close()


if __name__ == '__main__':
	main()
