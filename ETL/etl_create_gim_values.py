from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
from sklearn import preprocessing
import datetime
import pandas as pd
import numpy as np
from pickle import load
import torch
import torch.nn as nn
import torch.nn.functional as F

# REMOVED CUDA TO MAKE IT WORK ON RASPBERRY PI, SEE LINE 221/222


def create_gim_values():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()

    # Getting the most recent run
    mostRecentRun = pd.read_sql_query("select date from script_execution where script = 'create_gim_values' order by date desc limit 1",
                                      connection)

    # If we've never run it before, we start from the beginning
    if len(mostRecentRun) == 0:
        date_time_str = '2000-10-04 01:55:19'
        mostRecentRun = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        mostRecentRun = mostRecentRun.date()
    else:
        # Otherwise just converting it into sql form
        # Converting it from np.datetime64 to datetime
        # CITATION: https://stackoverflow.com/questions/13703720/converting-between-datetime-timestamp-and-datetime64
        mostRecentRun = (mostRecentRun['date'].values[0] - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
        mostRecentRun = datetime.datetime.utcfromtimestamp(mostRecentRun)  # Adding one day on since we already ran it
        mostRecentRun = mostRecentRun.date()

    # Getting all the games we need to get the live data for (i.e. everything from our last run up to games played yesterday)
    print('Loading Data')
    sequenceData = pd.read_sql_query(f"""
                                            select gim_sequences.*
                                            from stage_hockey.gim_sequences inner join hockey.schedules on gim_sequences.gameID = schedules.gameID where gameDate >= '{mostRecentRun}'
                                     """, connection)

    # Closing the connection as it is no longer needed
    connection.close()
    if len(sequenceData) == 0:
        return 0

    colsTransformed = ['goalDiff',
                       'manpowerDiff',
                       'periodNum',
                       'secondsElapsed',
                       'xCoord',
                       'yCoord']

    scaler = load(open('ETL/gim_scaler.pkl', 'rb'))

    scaledData = scaler.transform(sequenceData[colsTransformed].values)

    for i in range(0, len(colsTransformed)):
        sequenceData[colsTransformed[i]] = scaledData[:, i]

    # Defining a sequence data object
    sequenceDataTMinusOne = sequenceData.drop(['goalDiff', 'manpowerDiff', 'periodNum'], axis=1).copy(deep=True)

    # Incrementing the eventnumber to use to join below
    sequenceDataTMinusOne['eventNum'] -= 1

    # Merging the time t and t+1 datasets
    sequenceDataComplete = pd.merge(left=sequenceData,
                                    right=sequenceDataTMinusOne,
                                    how='left',
                                    left_on=['gameID', 'sequenceNum', 'eventNum'],
                                    right_on=['gameID', 'sequenceNum', 'eventNum'],
                                    suffixes=('', '_TMinusOne'))

    # Defining list of columns to ensure order is always consistent for the model
    columns = ['gameID',
               'sequenceNum',
               'eventNum',
               'goalDiff',
               'manpowerDiff',
               'periodNum',
               'secondsElapsed',
               'xCoord',
               'yCoord',
               'blocked_shot',
               'faceoff',
               'giveaway',
               'goal',
               'assist',
               'hit',
               'missed_shot',
               'penalty',
               'shot',
               'takeaway',
               'away',
               'home',
               'playerID',
               'secondsElapsed_TMinusOne',
               'xCoord_TMinusOne',
               'yCoord_TMinusOne',
               'blocked_shot_TMinusOne',
               'faceoff_TMinusOne',
               'giveaway_TMinusOne',
               'goal_TMinusOne',
               'assist_TMinusOne',
               'hit_TMinusOne',
               'missed_shot_TMinusOne',
               'penalty_TMinusOne',
               'shot_TMinusOne',
               'takeaway_TMinusOne',
               'away_TMinusOne',
               'home_TMinusOne']

    # Adding in any missing columns (setting them to be 0)
    for col in columns:
        if col not in sequenceDataComplete.columns:
            sequenceDataComplete[col] = np.zeros((len(sequenceDataComplete)))

    # Re-ordering columns
    sequenceDataComplete = sequenceDataComplete[columns]

    # Moving the df to GPU
    dfGPU = df_to_tensor(sequenceDataComplete)

    # Reshaping
    # (batch size, sequence length, num features)
    dfGPU = dfGPU.reshape((-1, 1, 37))

    # Loading model
    network = DQN()
    network.load_state_dict(torch.load('ETL/gim_model.pt'))
    network.eval()
    network.to(get_device())

    GIM = []
    # Each Episode
    for gameID in sequenceDataComplete['gameID'].unique():
        print(gameID)
        gameDataGPU = dfGPU[dfGPU[:, :, 0][:, 0] == gameID, :, :]
        gameData = sequenceDataComplete[sequenceDataComplete['gameID'] == gameID]
        for sequenceNum in gameData['sequenceNum'].unique():
            modelInput = gameDataGPU[gameDataGPU[:, :, 1][:, 0] == sequenceNum, :, :]
            i = 0
            while i < modelInput.shape[0]:
                if i == 0:
                    Q_t = network(modelInput[0:i + 1, :, 3:21])
                    gim_t = Q_t
                #                 print(modelInput[0:i+1,:,3:20])
                #                 print(Q_t)
                else:
                    Q_tMinusOne = Q_t
                    Q_t = network(modelInput[0:i + 1, :, 3:21])
                    #                 gim_t = Q_t - Q_tMinusOne
                    gim_t = Q_t
                GIM.append([int(modelInput[i, 0, 0].item()),  # GameID
                            int(modelInput[i, 0, 1].item()),  # sequenceNumber
                            int(modelInput[i, 0, 2].item()),  # eventNumber
                            modelInput[i, 0, 21].item(),  # PlayerID
                            modelInput[i, 0, 19].item(),  # Away
                            modelInput[i, 0, 20].item(),  # Home
                            gim_t[0, 0, 0].item(),  # Home Probability
                            gim_t[0, 0, 1].item(),  # Away Probability
                            gim_t[0, 0, 2].item()])  # Neither Probability
                i += 1

    results = pd.DataFrame(GIM, columns=['gameID',
                                         'sequenceNum',
                                         'eventNum',
                                         'playerID',
                                         'awayTeam',
                                         'homeTeam',
                                         'homeProbability',
                                         'awayProbability',
                                         'neitherProbability'])

    # Opening new connection to dump the new data
    conn = DatabaseConnection.sql_connection(creds.server, 'stage_hockey', creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()
    for index, row in results.iterrows():
        query = f"insert into stage_hockey.gim_values values ({row['gameID']}," \
                f"{row['sequenceNum']}," \
                f"{row['eventNum']}," \
                f"{row['playerID']}," \
                f"{row['awayTeam']}," \
                f"{row['homeTeam']}," \
                f"{row['homeProbability']}," \
                f"{row['awayProbability']}," \
                f"{row['neitherProbability']})"
        cursor.execute(query)
        connection.commit()
    connection.close()


class DQN(nn.Module):
    def __init__(self):
        super().__init__()
        self.inputSize = 18
        self.numLSTMNodes = 1000
        self.numLSTMLayers = 1

        self.lstmLayer = nn.LSTM(input_size=self.inputSize,
                                 hidden_size=self.numLSTMNodes,
                                 num_layers=self.numLSTMLayers,
                                 bias=True,
                                 dropout=0,
                                 batch_first=True).double()
        self.hidden1 = nn.Linear(in_features=self.numLSTMNodes, out_features=1000).double()
        self.hidden2 = nn.Linear(in_features=1000, out_features=1000).double()
        self.hidden3 = nn.Linear(in_features=1000, out_features=1000).double()
        self.hidden4 = nn.Linear(in_features=1000, out_features=1000).double()
        self.output = nn.Linear(in_features=1000, out_features=3).double()

    def forward(self, modelInput):
        hidden = (
            # torch.cuda.FloatTensor(self.numLSTMLayers, 1, self.numLSTMNodes).normal_().double(),
            # torch.cuda.FloatTensor(self.numLSTMLayers, 1, self.numLSTMNodes).normal_().double()
            torch.FloatTensor(self.numLSTMLayers, 1, self.numLSTMNodes).normal_().double(),
            torch.FloatTensor(self.numLSTMLayers, 1, self.numLSTMNodes).normal_().double()
        )
        for sequence in modelInput:
            out, hidden = self.lstmLayer(sequence.view(1, 1, -1), hidden)
        t = F.relu(out)
        t = F.relu(self.hidden1(t))
        t = F.relu(self.hidden2(t))
        t = F.relu(self.hidden3(t))
        t = F.relu(self.hidden4(t))
        t = F.softmax(self.output(t), dim=2)
        return t


def get_device():
    if torch.cuda.is_available():
        device = torch.device('cuda:0')
    else:
        device = torch.device('cpu')  # don't have GPU
    return device


# convert a df to tensor to be used in pytorch
def df_to_tensor(df):
    device = get_device()
    data = torch.from_numpy(df.values)
    data = data.type(torch.float64)
    data = data.to(device)
    return data
