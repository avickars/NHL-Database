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




 -- Number of assists,goals and shots by player, game, season and team (for regular season)
drop view if exists game_sheet;
create view game_sheet as
select COALESCE(assists.seasonID, goals.seasonID, shots.seasonID, penalties.seasonID, faceOffs.seasonID, specialGoals.seasonID, specialAssists.seasonID, overTimeGoals.seasonID, overTimeAssists.seasonID, 'N/A') as 'seasonID',
       COALESCE(assists.gameID, goals.gameID, shots.gameID, penalties.gameID, faceOffs.gameID, specialGoals.gameID, specialAssists.gameID, overTimeGoals.gameID, overTimeAssists.gameID, 'N/A') as 'gameID',
       COALESCE(assists.teamID, goals.teamID, shots.teamID, penalties.teamID, faceOffs.teamID, specialGoals.teamID, specialAssists.teamID, overTimeGoals.teamID, overTimeAssists.teamID, 'N/A') as 'teamID',
       COALESCE(assists.playerID, goals.playerID, shots.playerID, penalties.playerID, faceOffs.playerID, specialGoals.playerID, specialAssists.playerID, overTimeGoals.playerID, overTimeAssists.playerID, 'N/A') as 'playerID',
       ISNULL(goals.goals, 0) as 'G', -- goals
       ISNULL(assists.assists, 0) as 'A', -- assists
       ISNULL(assists.assists, 0) + ISNULL(goals.goals, 0) as 'P', -- points
       ISNULL(shots.shots, 0) as 'S', -- num shots
       CONVERT(float, ISNULL(goals.goals, 0)) / NULLIF((CONVERT(float, ISNULL(shots.shots, 0)) + CONVERT(float, ISNULL(goals.goals, 0))),0) as 'S%', -- shooting percentage
       ISNULL(penalties.PIM, 0) as 'PIM', -- penalty minutes
       ISNULL(faceOffs.numWins, 0) as 'FOW', -- face off wins
       ISNULL(faceOffs.numLosses, 0) as 'FOL', -- face off losses
       CONVERT(float, ISNULL(faceOffs.numWins, 0))/NULLIF((CONVERT(float, ISNULL(faceOffs.numWins, 0)) + CONVERT(float, ISNULL(faceOffs.numLosses, 0))),0) as 'FO%', -- face off winning percentage
       COALESCE(assists.gameType, goals.gameType, shots.gameType, penalties.gameType, faceOffs.gameType, specialGoals.gameType, specialAssists.gameType, overTimeGoals.gameType, overTimeAssists.gameType, 'N/A') as 'gameType',
       ISNULL(specialGoals.PPG, 0) as 'PPG', -- powerplay goal
       ISNULL(specialAssists.PPA, 0) as 'PPA', -- powerplay assist
       ISNULL(specialGoals.PPG, 0) + ISNULL(specialAssists.PPA, 0) as 'PPP', -- powerplay points
       ISNULL(specialGoals.ESG, 0) as 'ESG', -- even strength goal
       ISNULL(specialAssists.ESA, 0) as 'ESA', -- even strength assist
       ISNULL(specialGoals.ESG, 0) + ISNULL(specialAssists.ESA, 0) as 'EVP', --- even strength points
       ISNULL(specialGoals.SHG, 0) as 'SHG', -- short handed goal
       ISNULL(specialAssists.SHA, 0) as 'SHA', -- short handed assist
       ISNULL(specialGoals.SHG, 0) + ISNULL(specialAssists.SHA, 0) as 'SHP', --shorthanded points
       ISNULL(overTimeGoals.OTG, 0) as 'OTG', -- over time goals
       ISNULL(overTimeAssists.OTA, 0) as 'OTA', -- over time assists
       ISNULL(overTimeGoals.OTG, 0)  + ISNULL(overTimeAssists.OTA, 0) as 'OTP' -- over time points
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
              lf.playerType = 'Scorer'
        group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID
    ) goals on assists.playerID = goals.playerID and
               assists.seasonID = goals.seasonID and
               assists.teamID = goals.teamID and
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
              lf.playerType = 'Shooter'
        group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID
    ) shots on goals.playerID = shots.playerID and
               goals.seasonID = shots.seasonID and
               goals.teamID = shots.teamID and
               goals.gameID = shots.gameID
full outer join
    (
        select lf.playerID,
               s.gameType,
               lf.gameID,
               s.seasonID,
               sum(penaltyMinutes) as 'PIM',
               lf.teamID
        from live_feed_temp lf
        inner join schedules s on lf.gameID = s.gameID
        where lf.eventTypeID = 'PENALTY' and
              lf.playerType = 'PenaltyOn'
        group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID
    ) penalties on shots.playerID = penalties.playerID and
                   shots.seasonID = penalties.seasonID and
                   shots.teamID = penalties.teamID and
                   shots.gameID = penalties.gameID
full outer join
    (
        -- Number of faceOff wins, losses, percentage by player, Game and season.   Note we pivot it so the number of wins/losses are in the same row (need for percentage)
        select seasonID,
               gameID,
               teamID,
               playerID,
               gameType,
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
                        lf.numEvents,
                        s.gameType
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
    ) as faceOffs on penalties.playerID = faceOffs.playerID and
                     penalties.seasonID = faceOffs.seasonID and
                     penalties.teamID = faceOffs.teamID and
                     penalties.gameID = faceOffs.gameID
full outer join
    (
        select playerID,
               gameType,
               gameID,
               seasonID,
               teamID,
               ISNULL(EVEN, 0) as 'ESG',
               ISNULL(PPG, 0) as 'PPG',
               ISNULL(SSH, 0) as 'SHG'
        from
             (
                 select lf.playerID,
                        s.gameType,
                        lf.gameID,
                        s.seasonID,
                        count(*) as 'goals',
                        lf.teamID,
                        lf.strength
                 from live_feed_temp lf
                 inner join schedules s on s.gameID = lf.gameID
                 where lf.eventTypeID = 'GOAL' and
                       lf.playerType = 'Scorer'
                 group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID, lf.strength
             ) as sourceTable
        pivot
             (
                 sum(goals) for strength in ("EVEN", "PPG","SSH")
             ) as pivotTable

    ) as specialGoals on specialGoals.playerID = faceOffs.playerID and
                           specialGoals.seasonID = faceOffs.seasonID and
                           specialGoals.teamID = faceOffs.teamID and
                           specialGoals.gameID = faceOffs.gameID
full outer join
    (
        select playerID,
               gameType,
               gameID,
               seasonID,
               teamID,
               ISNULL(EVEN, 0) as 'ESA',
               ISNULL(PPG, 0) as 'PPA',
               ISNULL(SSH, 0) as 'SHA'
        from
             (
                 select lf.playerID,
                        s.gameType,
                        lf.gameID,
                        s.seasonID,
                        count(*) as 'assists',
                        lf.teamID,
                        lf.strength
                 from live_feed_temp lf
                 inner join schedules s on s.gameID = lf.gameID
                 where lf.eventTypeID = 'GOAL' and
                       lf.playerType = 'Assist'
                 group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID, lf.strength
             ) as sourceTable
        pivot
             (
                 sum(assists) for strength in ("EVEN", "PPG","SSH")
             ) as pivotTable
        ) as specialAssists on specialAssists.playerID = specialGoals.playerID and
                               specialAssists.seasonID = specialGoals.seasonID and
                               specialAssists.teamID = specialGoals.teamID and
                               specialAssists.gameID = specialGoals.gameID
full outer join
    (
        -- getting playoff overtime goals
        select lf.playerID,
                       s.gameType,
                       lf.gameID,
                       s.seasonID,
                       count(*)  as 'OTG',
                       lf.teamID
                from live_feed_temp lf
                inner join schedules s on s.gameID = lf.gameID
                where lf.eventTypeID = 'GOAL' and
                      lf.playerType = 'Scorer' and
                      lf.periodNum > 3 and gameType='P'
                group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID, periodNum
        union
        -- Getting regular and preseason season overtime goals
        select lf.playerID,
                       s.gameType,
                       lf.gameID,
                       s.seasonID,
                       count(*)  as 'OTG',
                       lf.teamID
                from live_feed_temp lf
                inner join schedules s on s.gameID = lf.gameID
                where lf.eventTypeID = 'GOAL' and
                      lf.playerType = 'Scorer' and
                      lf.periodNum = 4 and (gameType='R' or gameType = 'PR')
                group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID, periodNum
    ) as overTimeGoals on overTimeGoals.playerID = specialAssists.playerID and
                          overTimeGoals.seasonID = specialAssists.seasonID and
                          overTimeGoals.teamID = specialAssists.teamID and
                          overTimeGoals.gameID = specialAssists.gameID
full outer join
    (
        -- getting playoff overtime goals
        select lf.playerID,
                       s.gameType,
                       lf.gameID,
                       s.seasonID,
                       count(*)  as 'OTA',
                       lf.teamID
                from live_feed_temp lf
                inner join schedules s on s.gameID = lf.gameID
                where lf.eventTypeID = 'GOAL' and
                      lf.playerType = 'Assist' and
                      lf.periodNum > 3 and gameType='P'
                group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID, periodNum
        union
        -- Getting regular and preseason season overtime goals
        select lf.playerID,
                       s.gameType,
                       lf.gameID,
                       s.seasonID,
                       count(*)  as 'OTA',
                       lf.teamID
                from live_feed_temp lf
                inner join schedules s on s.gameID = lf.gameID
                where lf.eventTypeID = 'GOAL' and
                      lf.playerType = 'Assist' and
                      lf.periodNum = 4 and (gameType='R' or gameType = 'PR')
                group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID, periodNum
    ) as overTimeAssists on overTimeAssists .playerID = overTimeGoals.playerID and
                          overTimeAssists .seasonID = overTimeGoals.seasonID and
                          overTimeAssists .teamID = overTimeGoals.teamID and
                          overTimeAssists .gameID = overTimeGoals.gameID







select * from live_feed_temp where eventTypeID = 'GOAL'



























-- tests if the time is greater
create function is_time_greater (
    @greaterMinutesElapsed int,
    @greaterSecondsElapsed int,
    @lessMinutesElapsed int,
    @lessSecondsElapsed int
)
returns bit
as
    begin
        return IIF(@greaterMinutesElapsed = @lessMinutesElapsed and @greaterSecondsElapsed >= @lessSecondsElapsed, 1,
                    IIF(@greaterMinutesElapsed > @lessMinutesElapsed,1,0))
    end

-- tests if the time is less
create function is_time_less (
    @lessMinutesElapsed int,
    @lessSecondsElapsed int,
    @greaterMinutesElapsed int,
    @greaterSecondsElapsed int
)
returns bit
as
    begin
        return IIF(@lessMinutesElapsed = @greaterMinutesElapsed and @lessSecondsElapsed <= @greaterSecondsElapsed, 1,
                    IIF(@lessMinutesElapsed < @greaterMinutesElapsed, 1, 0))
    end

































