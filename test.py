import requests

url_string = f"https://statsapi.web.nhl.com/api/v1/game/2000020019/feed/live"
url = requests.get(url_string)
url_data = url.json()
gameID = 2000020019

for event in url_data['liveData']['plays']['allPlays']:

    playerID = []
    playerType = []
    for player in event['players']:
        try:
            playerID.append(player['player']['id'])
        except IndexError:
            playerID.append('NULL')
        except KeyError:
            playerID.append('NULL')
        try:
            playerType.append(player['playerType'])
        except IndexError:
            playerType.append('NULL')
        except KeyError:
            playerType.append('NULL')

    try:
        gameEvent = f"\'{event['result']['event']}\'"
    except KeyError:
        gameEvent = 'NULL'

    try:
        eventCode = f"\'{event['result']['eventCode']}\'"
    except KeyError:
        eventCode = 'NULL'

    try:
        eventTypeID = f"\'{event['result']['eventTypeId']}\'"
    except KeyError:
        eventTypeID = 'NULLeventTypeID'

    try:
        eventDescription = f"\'{event['result']['description']}\'"
    except KeyError:
        eventDescription = 'NULL'

    try:
        secondaryType = f"\'{event['result']['secondaryType']}\'"
    except KeyError:
        secondaryType = 'NULL'

    try:
        periodNum = event['about']['period']
    except KeyError:
        periodNum = 'NULL'

    eventID = event['about']['eventId']

    try:
        periodTime = f"\'{event['about']['periodTime']}\'"
    except KeyError:
        periodTime = 'NULL'

    try:
        xCoordinate = event['coordinates']['x']
    except KeyError:
        xCoordinate = 'NULL'

    try:
        yCoordinate = event['coordinates']['y']
    except KeyError:
        yCoordinate = 'NULL'

    for i in range(0,len(playerID)):
        query = f"insert into live_feed values (" \
                f"{eventID}," \
                f"{gameID}," \
                f"{gameEvent}," \
                f"{eventCode}," \
                f"{eventTypeID}," \
                f"{eventDescription}," \
                f"{secondaryType}," \
                f"{periodNum}," \
                f"{periodTime}," \
                f"{playerID[i]}," \
                f"{playerType[i]}," \
                f"{xCoordinate}," \
                f"{yCoordinate})"
        print(query)