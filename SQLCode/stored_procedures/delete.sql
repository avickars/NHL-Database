select bs.gameID,
       bs.teamID,
       bs.playerID,
       IFNULL(bs.jerseyNumber, 'N/A') as 'Jersery Number',
       IFNULL(bs.timeOnIce, '0:00') as 'TOI',
       IFNULL(bs.plusMinus, 0) as '+\-',
       IFNULL(bs.evenTimeOnIce, '0:00') as 'ESTOI',
       IFNULL(bs.powerPlayTimeOnIce, '0:00') as 'PPTOI',
       IFNULL(bs.shortHandedTimeOnIce, '0:00') as 'SHTOI',
       IF(bs.unknown = 1, 'Yes', IF(bs.unknown = 0, 'No', IFNULL(bs.unknown, 'N/A'))) as 'Status Unknown',
       IF(bs.scratched = 1, 'Yes', IF(bs.scratched= 0, 'No', IFNULL(bs.scratched, 'N/A'))) as 'Scratched',
       IFNULL(playerInfo.shots, 0) as 'S',
       IFNULL(playerInfo.evenStrengthGoals, 0) as 'ESG',
       IFNULL(playerInfo.shortHandedGoals, 0) as 'SHG',
       IFNULL(playerInfo.powerPlayGoals, 0) as 'PPG',
       IFNULL(playerInfo.evenStrengthAssists, 0) as 'ESA',
       IFNULL(playerInfo.shortHandedAssists, 0) as 'SHA',
       IFNULL(playerInfo.powerPlayAssists, 0) as 'PPA',
       IFNULL(playerInfo.takeaways, 0) as 'T',
       IFNULL(playerInfo.giveaways, 0) as 'GA',
       IFNULL(playerInfo.hitsGiven, 0) as 'HG',
       IFNULL(playerInfo.hitsTaken, 0) as 'HT',
       IFNULL(playerInfo.faceOffWins, 0) as 'FOW',
       IFNULL(playerInfo.faceOffLoses, 0) as 'FOL',
       IFNULL(playerInfo.numBlockedShots, 0) as 'BS',
       IFNULL(playerInfo.numShotsBlocked, 0) as 'SB',
       IFNULL(playerInfo.numMissedShots, 0) as 'MS',
       IFNULL(playerInfo.penaltyMinutesTaken, 0) as 'PIMT',
       IFNULL(playerInfo.penaltiesTaken, 0) as 'PIT',
       IFNULL(playerInfo.penaltyMinutesDrawn, 0) as 'PIMD',
       IFNULL(playerInfo.penaltiesDrawn, 0) as 'PID'
from box_scores bs
left join
     (
         select playerID,
                teamID,
                gameID,
                gameType,
                SUM(IF(eventTypeID = 'SHOT' and playerType = 'Shooter', count, 0))                     'shots',
                SUM(IF(eventTypeID = 'GOAL' and playerType = 'Scorer' and strength = 'EVEN', count,
                       0))                                                                             'evenStrengthGoals',
                SUM(IF(eventTypeID = 'GOAL' and playerType = 'Scorer' and strength = 'PPG', count, 0)) 'powerPlayGoals',
                SUM(IF(eventTypeID = 'GOAL' and playerType = 'Scorer' and strength = 'SHG', count,
                       0))                                                                             'shortHandedGoals',
                SUM(IF(eventTypeID = 'GOAL' and playerType = 'Assist' and strength = 'EVEN', count,
                       0))                                                                             'evenStrengthAssists',
                SUM(IF(eventTypeID = 'GOAL' and playerType = 'Assist' and strength = 'PPG', count,
                       0))                                                                             'powerPlayAssists',
                SUM(IF(eventTypeID = 'GOAL' and playerType = 'Assist' and strength = 'SHG', count,
                       0))                                                                             'shortHandedAssists',
                SUM(IF(eventTypeID = 'TAKEAWAY', count, 0))                                            'takeaways',
                SUM(IF(eventTypeID = 'GIVEAWAY', count, 0))                                            'giveaways',
                SUM(IF(eventTypeID = 'HIT' and playerType = 'Hitter', count, 0))                       'hitsGiven',
                SUM(IF(eventTypeID = 'HIT' and playerType = 'Hitter', count, 0))                       'hitsTaken',
                SUM(IF(eventTypeID = 'FACEOFF' and playerType = 'Winner', count, 0))                   'faceOffWins',
                SUM(IF(eventTypeID = 'FACEOFF' and playerType = 'Loser', count, 0))                    'faceOffLoses',
                SUM(
                        IF(eventTypeID = 'BLOCKED_SHOT' and playerType = 'BLOCKER', count, 0))         'numShotsBlocked',
                SUM(
                        IF(eventTypeID = 'BLOCKED_SHOT' and playerType = 'Shooter', count, 0))         'numBlockedShots',
                SUM(IF(eventTypeID = 'MISSED_SHOT' and playerType = 'Shooter', count, 0))              'numMissedShots',
                SUM(IF(eventTypeID = 'PENALTY' and playerType = 'PenaltyOn', sumPenaltyMinutes,
                       0))                                                                             'penaltyMinutesTaken',
                sum(IF(eventTypeID = 'PENALTY' and playerType = 'PenaltyOn', count, 0))                'penaltiesTaken',
                SUM(IF(eventTypeID = 'PENALTY' and playerType = 'DrewBy', sumPenaltyMinutes,
                       0))                                                                             'penaltyMinutesDrawn',
                SUM(IF(eventTypeID = 'PENALTY' and playerType = 'DrewBy', count, 0))                   'penaltiesDrawn'
         from (
                  select lf.playerID,
                         lf.teamID,
                         lf.gameID,
                         lf.eventTypeID,
                         lf.strength,
                         lf.playerType,
                         count(*)            as 'count',
                         sum(penaltyMinutes) as 'sumPenaltyMinutes',
                         gameType
                  from (
                           select lf.playerID,
                                  lf.gameID,
                                  lf.eventTypeID,
                                  lf.strength,
                                  lf.playerType,
                                  lf.penaltyMinutes,
                                  IF(lf.playerType in ('Loser', 'Hittee', 'DrewBy'),
                                     IF(lf.teamID = s.homeTeamID,
                                        s.awayTeamID,
                                        s.homeTeamID),
                                     lf.teamID) "teamID",
                                  s.gameType
                           from live_feed lf
                                    inner join schedules s on lf.gameID = s.gameID) lf
                  where (lf.eventTypeID = 'SHOT' and lf.playerType = 'Shooter')
                     or (lf.eventTypeID = 'GOAL' and lf.playerType = 'Scorer')
                     or (lf.eventTypeID = 'GOAL' and lf.playerType = 'Assist')
                     or (lf.eventTypeID = 'TAKEAWAY')
                     or (lf.eventTypeID = 'GIVEAWAY')
                     or (lf.eventTypeID = 'HIT' and lf.playerType = 'Hitter')
                     or (lf.eventTypeID = 'HIT' and lf.playerType = 'Hittee')
                     or (lf.eventTypeID = 'FACEOFF' and lf.playerType = 'Winner')
                     or (lf.eventTypeID = 'FACEOFF' and lf.playerType = 'Loser')
                     or (lf.eventTypeID = 'BLOCKED_SHOT' and lf.playerType = 'Blocker')
                     or (lf.eventTypeID = 'BLOCKED_SHOT' and lf.playerType = 'Shooter')
                     or (lf.eventTypeID = 'MISSED_SHOT' and lf.playerType = 'Shooter')
                     or (lf.eventTypeID = 'PENALTY' and lf.playerType = 'PenaltyOn')
                  group by lf.playerID,
                           lf.teamID,
                           lf.gameID,
                           lf.eventTypeID,
                           lf.strength,
                           lf.playerType,
                           lf.gameType) RAW
         group by playerID, teamID, gameID, gameType
     ) playerInfo on bs.gameID =  playerInfo.gameID and
                     bs.teamID = playerInfo.teamID and
                     bs.playerID = playerInfo.playerID


                     select * from live_feed_temp

select * from box_scores_temp








