CREATE procedure sp_game_prediction_team_stats_view()
begin

drop table if exists STATS;
create temporary table STATS
select s.seasonID,
      s.gameID,
      lf.teamID,
      SUM(IF(eventTypeID = 'GOAL', 1, 0)) AS 'goals',
      SUM(IF(eventTypeID = 'SHOT', 1, 0)) AS 'shots'
from live_feed lf
   inner join schedules s on lf.gameID = s.gameID
   left join box_scores bs on lf.gameID = bs.gameID and lf.playerID = bs.playerID
where
     seasonID>=20102011 and
     gameType = 'R'  and
     ((eventTypeID='GOAL' and playerType = 'Scorer') or (eventTypeID='SHOT' and playerType='Shooter'))
group by s.gameID,
      lf.teamID;

drop table if exists stage_hockey.game_prediction_team_stats;


create table stage_hockey.game_prediction_team_stats as
select seasonID,
    gameDate,
    gameType,
   gameID,
   teamID,
   shotsForTotal/gameNumber as 'shotsForPerGame',
   goalsForTotal/gameNumber as 'goalsForPerGame',
   shotsAgainstTotal/gameNumber as 'shotsAgainstPerGame',
   goalsAgainstTotal/gameNumber as 'goalsAgainstPerGame',
   winTotal/gameNumber as 'winningPercentage',
   shotsForTotal - shotsAgainstTotal as 'shotDifferential',
   goalsForTotal - goalsAgainstTotal as 'goalDifferential',
   gameNumber
from
   (
        select GAMES.seasonID,
               GAMES.gameID,
               GAMES.teamID,
               GAMES.gameDate,
               GAMES.gameType,
               ROW_NUMBER() over (partition by GAMES.seasonID, GAMES.teamID order by GAMES.gameID) as 'gameNumber',
               SUM(STATS_FOR.shots) over (partition by GAMES.seasonID, GAMES.teamID order by GAMES.gameID) 'shotsForTotal',
               SUM(STATS_FOR.goals) over (partition by GAMES.seasonID, GAMES.teamID order by GAMES.gameID) 'goalsForTotal',
               SUM(STATS_AGAINST.shots) over (partition by GAMES.seasonID, GAMES.teamID order by GAMES.gameID) 'shotsAgainstTotal',
               SUM(STATS_AGAINST.goals) over (partition by GAMES.seasonID, GAMES.teamID order by GAMES.gameID) 'goalsAgainstTotal',
               SUM(IF(STATS_FOR.goals > STATS_AGAINST.goals, 1, 0)) over (partition by GAMES.seasonID, GAMES.teamID order by GAMES.gameID) 'winTotal'
        from (
                select s.seasonID,
                       gameID,
                       homeTeamID as 'teamID',
                       s.gameDate,
                       s.gameType
                from schedules s
                where s.gameID >= 2020020001 and
                     seasonID>=20102011 and
                     gameType = 'R'
                union
                select seasonID,
                       gameID,
                       awayTeamID as 'teamID',
                       s.gameDate,
                       s.gameType
                from schedules s
                where seasonID>=20102011
             ) GAMES
        inner join STATS STATS_FOR on (GAMES.gameID = STATS_FOR.gameID and GAMES.teamID = STATS_FOR.teamID)
        inner join STATS STATS_AGAINST on (GAMES.gameID = STATS_AGAINST.gameID and GAMES.teamID <> STATS_AGAINST.teamID)
        order by GAMES.gameID, GAMES.teamID
) STATS;

end;
