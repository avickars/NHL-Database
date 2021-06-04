select *
from
    (
        select lf.playerID,
               s.gameType,
               lf.gameID,
               s.seasonID,
               count(*) as 'assists',
               lf.teamID
        from live_feed_temp lf
        inner join schedules s on s.gameID = lf.gameID
        where lf.eventTypeID = 'GOAL' and
              lf.playerType = 'Assist'
        group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID
     ) assists
inner join
    (
        select lf.playerID,
               s.gameType,
               lf.gameID,
               s.seasonID,
               count(*)  as 'goals',
               lf.teamID
        from live_feed_temp lf
        inner join schedules s on s.gameID = lf.gameID
        where lf.eventTypeID = 'GOAL' and
              lf.playerType = 'Scorer'
        group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID
    ) goals on assists.playerID = goals.playerID and
               assists.seasonID = goals.seasonID and
               assists.teamID = goals.teamID and
               assists.gameID = goals.gameID
-- where ISNULL(assists.playerID,1)<>1

select * from (
select count(*) as 'numGoals', playerID from live_feed_temp where eventTypeID='GOAL' and playerType='Scorer' group by playerID ) g
inner join (
select count(*) as 'numAssists', playerID from live_feed_temp where eventTypeID='GOAL' and playerType='Assist' group by playerID) a on a.playerID=g.playerID


select count(*) as 'numGoals', playerID from live_feed_temp where eventTypeID='GOAL' and playerType='Scorer' group by playerID

select count(*) as 'numAssists', playerID from live_feed_temp where eventTypeID='Assist' and playerType='Scorer' group by playerID