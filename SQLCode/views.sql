drop view if exists conferences_view;

create view conferences_view as
select c.conferenceName as 'Conference Name', c.abbreviation as 'Conference Abbreviation', c.conferenceID as 'Conference ID'
from conferences c
inner join conference_activity ca on c.conferenceID = ca.conferenceID
where ca.active = 1;

drop view if exists divisions_view;

create view divisions_view as
select d.conferenceID as 'Conference ID', d.divisionName as 'Division Name', d.abbreviation as 'Division Abbreviation', d.divisionID
from divisions d
inner join division_activity da on d.divisionID = da.divisionID
where da.active = 1;

drop view if exists teams_view;

create view teams_view as
select t.teamID as 'Team ID',
       t.locationName as 'Team Location Name',
       t.teamName as 'Team Name',
       t.abbreviation as 'Team Abbreviation',
       tv.venueCity as 'Venue City',
       tv.venueName as 'Venue Name',
       tv.timeZone as 'Venue Time Zone',
       f.firstSeasonID as 'First Season',
       da.divisionID as 'Division ID'
from teams t
inner join
    (select teamID
    from (select *,
                 row_number() over (partition by teamID order by date desc ) as rowNum
            from team_activity where active = 1 or teamID=55) r
    where r.rowNum = 1) ta
on t.teamID = ta.teamID
inner join
    (select teamID, divisionID
    from (select *,
             row_number() over (partition by teamID order by date desc ) as rowNum
        from team_plays_in_division) r where r.rowNum = 1) da
on t.teamID = da.teamID
inner join
    (select venueCity, venueName, timeZone, teamID
    from (select *,
                 row_number() over (partition by teamID order by date desc ) as rowNum
    from team_plays_in_venue) r where r.rowNum = 1) as tv
on t.teamID = tv.teamID
inner join franchises f on f.franchiseID = t.franchiseID;

drop table live_feed_temp;


-- Number of assists by player, game, gametype,season and team
select lf.playerID, s.gameType, lf.gameID, s.seasonID, count(*)  as 'assists', lf.teamID
    from live_feed_temp lf
    inner join schedules s
        on s.gameID = lf.gameID
    where lf.eventTypeID = 'GOAL' and
          lf.playerType = 'Assist' and
          (s.gameType = 'P' or s.gameType = 'R')
    group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID




-- All players play for by individual game (contains gameID, playerID, teamID)
drop view if exists plays_for;
create view plays_for as
select *
from (
select *,
    row_number() over (partition by playerID order by gameID desc ) as 'rowNum'
from (
select *
from
     (-- Goalie plays for
     select distinct lf.gameID,
                     lf.playerID,
                     iif(lf.teamID != s.homeTeamID, s.homeTeamID, s.awayTeamID) as 'teamID'
     from live_feed_temp lf
         inner join schedules s
             on s.gameID = lf.gameID
     where lf.eventTypeID='SHOT' and playerType = 'Goalie') g
union
    select *
    from
         ( -- Player plays for
        select distinct lf.gameID,
                        lf.playerID,
                        lf.teamID
        from live_feed_temp lf
        where (eventTypeID = 'FACEOFF' and playerType = 'Winner') or
              (eventTypeID = 'HIT' and playerType = 'HITTER') or
              (eventTypeID = 'PENALTY' and playerType = 'PenaltyOn') or
              (eventTypeID = 'GOAL' and (playerType = ' Scorer' or playerType = 'Assist')) or
              (eventTypeID = 'SHOT' and playerType = 'Shooter') or
              (eventTypeID = 'GIVEAWAY' and playerType = 'PlayerID') or
              (eventTypeID = 'MISSED_SHOT' and playerType = 'Missed Shot') or
              (eventTypeID = 'Takeaway' and playerType='PlayerID')) pf) r) r2
where r2.rowNum=1


select lf.playerID,
        s.gameType,
        lf.gameID,
        s.seasonID,
        count(*) as 'penalty',
        lf.teamID
from live_feed_temp lf
inner join schedules s on lf.gameID = s.gameID
where lf.eventTypeID = 'PENALTY' and
      lf.playerType = 'PenaltyOn' and
      s.gameType = 'R'
group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID


 -- Number of assists,goals and shots by player, game, season and team (for regular season)
select ISNULL(assists.playerID, ISNULL(goals.playerID, ISNULL(shots.playerID, ISNULL(penalties.playerID, faceOffs.seasonID)))) as 'playerID',
       ISNULL(assists.seasonID, ISNULL(goals.seasonID, ISNULL(shots.seasonID, ISNULL(penalties.seasonID, faceOffs.seasonID)))) as 'seasonID',
       ISNULL(assists.teamID, ISNULL(goals.teamID, ISNULL(shots.teamID, ISNULL(penalties.teamID, faceOffs.teamID)))) as 'teamID',
       ISNULL(assists.assists, 0) as 'assists',
       ISNULL(goals.goals, 0) as 'goals',
       ISNULL(assists.assists, 0) + ISNULL(goals.goals, 0) as 'points',
       ISNULL(shots.shots, 0) as 'shots',
       ISNULL(penalties.penalty, 0) as 'penalties',
       ISNULL(assists.gameID, ISNULL(goals.gameID, ISNULL(shots.gameID, ISNULL(penalties.gameID, faceOffs.seasonID)))) as 'gameID',
       ISNULL(faceOffs.numWins, 0) as 'numFaceOffWins',
       ISNULL(faceOffs.numLosses, 0) as 'numFaceOffLosses'
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
              lf.playerType = 'Assist' and
              s.gameType = 'R'
        group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID
     ) assists
full outer join
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
              lf.playerType = 'Scorer' and
              s.gameType = 'R'
        group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID
    ) goals on assists.playerID = goals.playerID and
               assists.seasonID = goals.seasonID and
               assists.teamID = goals.seasonID and
               assists.gameID = goals.gameID
full outer join
    (
        select lf.playerID,
            s.gameType,
            lf.gameID,
            s.seasonID,
            count(*) as 'shots',
            lf.teamID
        from live_feed_temp lf
        inner join schedules s on lf.gameID = s.gameID
        where lf.eventTypeID = 'SHOT' and
              lf.playerType = 'Shooter' and
              s.gameType = 'R'
        group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID
    ) shots on goals.playerID = shots.playerID and
               goals.seasonID = shots.seasonID and
               goals.teamID = shots.seasonID and
               goals.gameID = shots.gameID
full outer join
    (
        select lf.playerID,
               s.gameType,
               lf.gameID,
               s.seasonID,
               count(*) as 'penalty',
               lf.teamID
        from live_feed_temp lf
        inner join schedules s on lf.gameID = s.gameID
        where lf.eventTypeID = 'PENALTY' and
              lf.playerType = 'PenaltyOn' and
              s.gameType = 'R'
        group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID
    ) penalties on assists.playerID = penalties.playerID and
                   assists.seasonID = penalties.seasonID and
                   assists.teamID = penalties.seasonID and
                   assists.gameID = penalties.gameID
full outer join
    (
        -- Number of faceOff wins, losses, percentage by player, Game and season.   Note we pivot it so the number of wins/losses are in the same row (need for percentage)
        select seasonID,
               gameID,
               teamID,
               playerID,
               isnull(Loser, 0) as 'numLosses',
               isnull(Winner, 0) as 'numWins'
               --     cast(sum(p.numWins) as float)/(cast(sum(p.numLosses) as float) + cast(sum(p.numWins) as float)) as 'faceOffPercentage'
        from
             (
                 -- Number of face-off wins/losses by player, and game, and team
                 select s.seasonID,
                        s.gameID,
                        IIF(lf.playerType = 'Winner', lf.teamID, IIF(lf.teamID = s.homeTeamID, s.awayTeamID, s.homeTeamID)) as 'teamID',
                        lf.playerID,
                        lf.playerType,
                        lf.numEvents
                 from
                      (
                          select teamID,
                                 gameID,
                                 playerType,
                                 playerID,
                                 count(playerType) as 'numEvents'
                          from live_feed_temp
                          where eventTypeID = 'FACEOFF'
                          group by playerType, playerID, gameID,teamID
                     ) lf
                 inner join schedules s on lf.gameID = s.gameID
             ) as sourceTable
        pivot
             (
                sum(numEvents) for playerType in ("Loser", "Winner")
             ) as pivotTable
    ) as faceOffs on assists.playerID = faceOffs.playerID and
                     assists.seasonID = faceOffs.seasonID and
                     assists.teamID = faceOffs.teamID and
                     assists.gameID = faceOffs.gameID


select * from live_feed_temp where eventTypeID = 'GOAL'































