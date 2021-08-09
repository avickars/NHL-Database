CREATE procedure sp_goalie_game_data_view()
begin
drop table if exists production_hockey.goalies_boxscores;
create table production_hockey.goalies_boxscores as
select bs.*,
       1 as 'GP',
       goalsSaves.ESG, -- evenstrength goals
       goalsSaves.PPG, -- powerplay goals
       goalsSaves.SHG, -- short handed goals
       goalsSaves.S, -- shots
       IF((homeTeamGoals > awayTeamGoals and goalsSaves.teamID = outcome.homeTeamID) or (awayTeamGoals > homeTeamGoals and goalsSaves.teamID = outcome.awayTeamID), 1, 0)  as 'W', -- wins
       IF((homeTeamGoals < awayTeamGoals and goalsSaves.teamID = outcome.homeTeamID) or (awayTeamGoals < homeTeamGoals and goalsSaves.teamID = outcome.awayTeamID), 1, 0)  as 'L', -- losses
       IF(homeTeamGoals = awayTeamGoals, 1, 0)  as 'T', -- ties
       IF((awayTeamGoals = 0 and goalsSaves.teamID = outcome.homeTeamID) or (homeTeamGoals = 0 and goalsSaves.teamID = outcome.awayTeamID), 1, 0) as 'SO', -- shutouts
        ROW_NUMBER() over (partition by bs.gameID,bs.playerID order by bs.gameID desc) AS 'gameNum'
from
     (
         select gameID,
               teamID,
               bs.playerID,
               jerseyNumber,
               timeOnIce,
               unknown,
               scratched
        from box_scores bs
        inner join
            (
                select playerID,
                       primaryPositionCode,
                       max(date)
                from plays_position
                where primaryPositionCode = 'G' group by playerID
            ) goalies on bs.playerID = goalies.playerID
        where timeOnIce > '0:00'
     ) bs
left join
     (
-- goals and saves
         select gameID,
                playerID,
                teamID,
                SUM(IF(eventTypeID = 'GOAL' and playerType = 'GOALIE' and strength = 'EVEN', count, 0)) as 'ESG',
                SUM(IF(eventTypeID = 'GOAL' and playerType = 'GOALIE' and strength = 'PPG', count, 0))  as 'PPG',
                SUM(IF(eventTypeID = 'GOAL' and playerType = 'GOALIE' and strength = 'SHG', count, 0))  as 'SHG',
                SUM(IF(eventTypeID = 'SHOT' and playerType = 'GOALIE', count, 0))                       as 'S'
         from (
                  select lf.playerID,
                         lf.teamID,
                         lf.gameID,
                         lf.eventTypeID,
                         lf.strength,
                         lf.playerType,
                         count(*) as 'count'
                  from (
                           select lf.playerID,
                                  lf.gameID,
                                  lf.eventTypeID,
                                  lf.strength,
                                  lf.playerType,
                                  IF(lf.playerType in ('Goalie'),
                                     IF(lf.teamID = s.homeTeamID,
                                        s.awayTeamID,
                                        s.homeTeamID),
                                     lf.teamID) "teamID",
                                  s.gameType
                           from live_feed lf
                                    inner join schedules s on lf.gameID = s.gameID
                       ) lf
                  where (eventTypeID = 'GOAL' and playerType = 'Goalie')
                     or (eventTypeID = 'SHOT' and playerType = 'Goalie')
                  group by lf.playerID,
                           lf.teamID,
                           lf.gameID,
                           lf.eventTypeID,
                           lf.strength,
                           lf.playerType
              ) rawCounts
         group by playerID, gameID, teamID
     ) goalsSaves on bs.gameID = goalsSaves.gameID and
                     bs.teamID = goalsSaves.teamID and
                     bs.playerID = goalsSaves.playerID
left join
     (
         select lf.gameID,
               s.homeTeamID,
               s.awayTeamID,
               SUM(IF(lf.teamID = s.homeTeamID, numGoals, 0)) as 'homeTeamGoals',
               SUM(IF(lf.teamID = s.awayTeamID, numGoals, 0)) as 'awayTeamGoals'
        from (
        select lf.gameID,
               lf.teamID,
               count(*) as 'numGoals'
        from live_feed lf
        where eventTypeID = 'GOAL' and eventSubID=0
        group by lf.gameID, lf.teamID ) lf
            inner join schedules s on lf.gameID = s.gameID
        group by lf.gameID, s.homeTeamID, s.awayTeamID
    ) outcome on  bs.gameID = outcome.gameID;
end

