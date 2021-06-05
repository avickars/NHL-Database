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




 -- Number of assists,goals and shots, etc by player, game, season and team (for regular season)
-- drop view if exists game_sheet;
-- create view game_sheet as
select seasonID,
       gameID,
       gameType,
       teamID,
       playerID,
       G, -- goals
       A, -- assists
       G + A as 'P', -- points
       S, -- shots
       CONVERT(float, G) / CONVERT(float, S) as 'S%', -- shot percentage
       PIM, -- penalty minutes
       FOW, -- face off wins
       FOL, -- face off losses
       CONVERT(float, FOW) / (CONVERT(float, FOW) + CONVERT(float, FOL)) as 'FO%', -- face off percentage
       ESG, -- evenstrength goals
       PPG, -- powerplay goals
       SHG, -- short handed goals
       ESA, -- even strength assists
       PPA, -- power play assists
       SHA, -- short handed assists
       OTG, -- over time goals
       OTA, -- over time assists
       Number, -- jersey number
       TOI, -- time on ice
       PPTOI, -- powerplay time on ice
       SHTOI, -- shorthanded time on ice
       [Status Unknown], -- game status unknown
       Scratched, -- scratched
       [+/-] -- plus/minus
from
     (
         select COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.seasonID, boxscores.seasonID, -1) as 'seasonID',
                COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.gameID, boxscores.gameID, -1) as 'gameID',
                COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.gameType, boxscores.gameType, 'N/A') as 'gameType',
                COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.teamID, boxscores.teamID, -1) as 'teamID',
                COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.playerID, boxscores.playerID, -1) as 'playerID',
                ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.G, 0) as 'G',
                ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.A, 0) as 'A',
                ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.S, 0) as 'S',
                ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.PIM, 0) as 'PIM',
                ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.FOW, 0) as 'FOW',
                ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.FOL, 0) as 'FOL',
                ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.ESG, 0) as 'ESG',
                ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.PPG, 0) as 'PPG',
                ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.SHG, 0) as 'SHG',
                ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.ESA, 0) as 'ESA',
                ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.PPA, 0) as 'PPA',
                ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.SHA, 0) as 'SHA',
                ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.OTG, 0) as 'OTG',
                ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.OTA, 0) as 'OTA',
                ISNULL(boxscores.jerseyNumber, -1) as 'Number',
                ISNULL(boxscores.timeOnIce, 'N/A') as 'TOI',
                ISNULL(boxscores.powerPlayTimeOnIce, 'N/A') as 'PPTOI',
                ISNULL(boxscores.shortHandedTimeOnIce, 'N/A') as 'SHTOI',
                boxscores.unknown as 'Status Unknown',
                boxscores.scratched as 'Scratched',
                boxscores.plusMinus as '+/-'
         from
              (
                  select COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.seasonID, overTimeAssists.seasonID, -1) as 'seasonID',
                         COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.gameID, overTimeAssists.gameID, -1) as 'gameID',
                         COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.gameType, overTimeAssists.gameType, 'N/A') as 'gameType',
                         COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.teamID, overTimeAssists.teamID, -1) as 'teamID',
                         COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.playerID, overTimeAssists.playerID, -1) as 'playerID',
                         ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.G, 0) as 'G',
                         ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.A, 0) as 'A',
                         ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.S, 0) as 'S',
                         ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.PIM, 0) as 'PIM',
                         ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.FOW, 0) as 'FOW',
                         ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.FOL, 0) as 'FOL',
                         ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.ESG, 0) as 'ESG',
                         ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.PPG, 0) as 'PPG',
                         ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.SHG, 0) as 'SHG',
                         ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.ESA, 0) as 'ESA',
                         ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.PPA, 0) as 'PPA',
                         ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.SHA, 0) as 'SHA',
                         ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.OTG, 0) as 'OTG',
                         ISNULL(overTimeAssists.OTA, 0) as 'OTA'

                  from
                       (
                           -- selecting all the assists, goals, shots, penalty mins ,special goals, special assists, overtime goals and overtime assists by playerID,gameID, seasonID and teamID
                           select COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.seasonID, overTimeGoals.seasonID, -1) as 'seasonID',
                                  COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.gameID, overTimeGoals.gameID, -1) as 'gameID',
                                  COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.gameType, overTimeGoals.gameType, 'N/A') as 'gameType',
                                  COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.teamID, overTimeGoals.teamID, -1) as 'teamID',
                                  COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.playerID, overTimeGoals.playerID, -1) as 'playerID',
                                  ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.G, 0) as 'G',
                                  ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.A, 0) as 'A',
                                  ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.S, 0) as 'S',
                                  ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.PIM, 0) as 'PIM',
                                  ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.FOW, 0) as 'FOW',
                                  ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.FOL, 0) as 'FOL',
                                  ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.ESG, 0) as 'ESG',
                                  ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.PPG, 0) as 'PPG',
                                  ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.SHG, 0) as 'SHG',
                                  ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.ESA, 0) as 'ESA',
                                  ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.PPA, 0) as 'PPA',
                                  ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.SHA, 0) as 'SHA',
                                  ISNULL(overTimeGoals.OTG, 0) as 'OTG'
                           from
                                (
                                    -- selecting all the assists, goals, shots, penalty mins ,special goals, special assists and overtime goals by playerID,gameID, seasonID and teamID
                                    select COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals.seasonID, specialAssists.seasonID, -1) as 'seasonID',
                                           COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals.gameID, specialAssists.gameID, -1) as 'gameID',
                                           COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals.gameType, specialAssists.gameType, 'N/A') as 'gameType',
                                           COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals.teamID, specialAssists.teamID, -1) as 'teamID',
                                           COALESCE(assist_goals_shots_penalties_faceoffs_specialgoals.playerID, specialAssists.playerID, -1) as 'playerID',
                                           ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals.G, 0) as 'G',
                                           ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals.A, 0) as 'A',
                                           ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals.S, 0) as 'S',
                                           ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals.PIM, 0) as 'PIM',
                                           ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals.FOW, 0) as 'FOW',
                                           ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals.FOL, 0) as 'FOL',
                                           ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals.ESG, 0) as 'ESG',
                                           ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals.PPG, 0) as 'PPG',
                                           ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals.SHG, 0) as 'SHG',
                                           ISNULL(specialAssists.ESA, 0) as 'ESA',
                                           ISNULL(specialAssists.PPA, 0) as 'PPA',
                                           ISNULL(specialAssists.SHA, 0) as 'SHA'

                                    from
                                         (
                                             -- selecting all the assists, goals, shots, penalty mins ,special goals and special assists by playerID,gameID, seasonID and teamID
                                             select COALESCE(assist_goals_shots_penalties_faceoffs.seasonID, specialGoals.seasonID, -1) as 'seasonID',
                                                    COALESCE(assist_goals_shots_penalties_faceoffs.gameID, specialGoals.gameID, -1) as 'gameID',
                                                    COALESCE(assist_goals_shots_penalties_faceoffs.gameType, specialGoals.gameType, 'N/A') as 'gameType',
                                                    COALESCE(assist_goals_shots_penalties_faceoffs.teamID, specialGoals.teamID, -1) as 'teamID',
                                                    COALESCE(assist_goals_shots_penalties_faceoffs.playerID, specialGoals.playerID, -1) as 'playerID',
                                                    ISNULL(assist_goals_shots_penalties_faceoffs.G, 0) as 'G',
                                                    ISNULL(assist_goals_shots_penalties_faceoffs.A, 0) as 'A',
                                                    ISNULL(assist_goals_shots_penalties_faceoffs.S, 0) as 'S',
                                                    ISNULL(assist_goals_shots_penalties_faceoffs.PIM, 0) as 'PIM',
                                                    ISNULL(assist_goals_shots_penalties_faceoffs.FOW, 0) as 'FOW',
                                                    ISNULL(assist_goals_shots_penalties_faceoffs.FOL, 0) as 'FOL',
                                                    ISNULL(specialGoals.ESG, 0) as 'ESG',
                                                    ISNULL(specialGoals.PPG, 0) as 'PPG',
                                                    ISNULL(specialGoals.SHG, 0) as 'SHG'
                                             from
                                                  (
                                                      -- selecting all the assists, goals, shots, penalty mins and special goals by playerID,gameID, seasonID and teamID
                                                      select COALESCE(assist_goals_shots_penalties.seasonID, faceOffs.seasonID, -1) as 'seasonID',
                                                             COALESCE(assist_goals_shots_penalties.gameID, faceOffs.gameID, -1) as 'gameID',
                                                             COALESCE(assist_goals_shots_penalties.gameType, faceOffs.gameType, 'N/A') as 'gameType',
                                                             COALESCE(assist_goals_shots_penalties.teamID, faceOffs.teamID, -1) as 'teamID',
                                                             COALESCE(assist_goals_shots_penalties.playerID, faceOffs.playerID, -1) as 'playerID',
                                                             ISNULL(assist_goals_shots_penalties.G, 0) as 'G',
                                                             ISNULL(assist_goals_shots_penalties.A, 0) as 'A',
                                                             ISNULL(assist_goals_shots_penalties.S, 0) as 'S',
                                                             ISNULL(assist_goals_shots_penalties.PIM, 0) as 'PIM',
                                                             ISNULL(faceOffs.numWins, 0) as 'FOW',
                                                             ISNULL(faceOffs.numLosses, 0) as 'FOL'
                                                      from
                                                           (
                                                               -- selecting all the assists, goals, shots and penalty mins by playerID,gameID, seasonID and teamID
                                                               select COALESCE(assist_goals_shots.seasonID, penalties.seasonID, -1) as 'seasonID',
                                                                      COALESCE(assist_goals_shots.gameID, penalties.gameID, -1) as 'gameID',
                                                                      COALESCE(assist_goals_shots.gameType, penalties.gameType, 'N/A') as 'gameType',
                                                                      COALESCE(assist_goals_shots.teamID, penalties.teamID, -1) as 'teamID',
                                                                      COALESCE(assist_goals_shots.playerID, penalties.playerID, -1) as 'playerID',
                                                                      ISNULL(assist_goals_shots.G, 0) as 'G',
                                                                      ISNULL(assist_goals_shots.A, 0) as 'A',
                                                                      ISNULL(assist_goals_shots.S, 0) as 'S',
                                                                      ISNULL(penalties.PIM, 0) as 'PIM'
                                                               from
                                                                    (
                                                                        -- selecting all the assists, goals and shots by playerID,gameID, seasonID and teamID
                                                                        select COALESCE(assists_goals.seasonID, shots.seasonID, -1) as 'seasonID',
                                                                               COALESCE(assists_goals.gameID, shots.gameID, -1) as 'gameID',
                                                                               COALESCE(assists_goals.gameType, shots.gameType, 'N/A') as 'gameType',
                                                                               COALESCE(assists_goals.teamID, shots.teamID, -1) as 'teamID',
                                                                               COALESCE(assists_goals.playerID, shots.playerID, -1) as 'playerID',
                                                                               ISNULL(assists_goals.G, 0) as 'G',
                                                                               ISNULL(assists_goals.A, 0) as 'A',
                                                                               ISNULL(shots.shots, 0) as 'S'
                                                                        from
                                                                             (
                                                                                 -- selecting all the assists and goals by playerID,gameID, seasonID and teamID
                                                                                 select COALESCE(assists.seasonID, goals.seasonID, -1) as 'seasonID',
                                                                                        COALESCE(assists.gameID, goals.gameID, -1) as 'gameID',
                                                                                        COALESCE(assists.gameType, goals.gameType, 'N/A') as 'gameType',
                                                                                        COALESCE(assists.teamID, goals.teamID, -1) as 'teamID',
                                                                                        COALESCE(assists.playerID, goals.playerID, -1) as 'playerID',
                                                                                        ISNULL(goals.goals, 0) as 'G',
                                                                                        ISNULL(assists.assists, 0) as 'A'
                                                                                 from
                                                                                      (
                                                                                          -- selecting all the assists by playerID,gameID, seasonID and teamID
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
                                                                                         -- selecting all the goals by playerID,gameID, seasonID and teamID
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
                                                                                     ) goals on assists.seasonID = goals.seasonID and
                                                                                                assists.gameID = goals.gameID and
                                                                                                assists.teamID = goals.teamID and
                                                                                                assists.playerID = goals.playerID
                                                                             ) assists_goals
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
                                                                            ) shots on assists_goals.seasonID = shots.seasonID and
                                                                                       assists_goals.gameID = shots.gameID and
                                                                                       assists_goals.teamID = shots.teamID and
                                                                                       assists_goals.playerID = shots.playerID
                                                                    ) assist_goals_shots
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
                                                                   ) penalties on assist_goals_shots.seasonID = penalties.seasonID and
                                                                                  assist_goals_shots.gameID = penalties.gameID and
                                                                                 assist_goals_shots.teamID = penalties.teamID and
                                                                                  assist_goals_shots.playerID = penalties.playerID
                                                           ) assist_goals_shots_penalties
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
                                                          ) as faceOffs on assist_goals_shots_penalties.seasonID = faceOffs.seasonID and
                                                                           assist_goals_shots_penalties.gameID = faceOffs.gameID and
                                                                           assist_goals_shots_penalties.teamID = faceOffs.teamID and
                                                                           assist_goals_shots_penalties.playerID = faceOffs.playerID
                                                  ) assist_goals_shots_penalties_faceoffs
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

                                                 ) as specialGoals on assist_goals_shots_penalties_faceoffs.seasonID = specialGoals.seasonID and
                                                                      assist_goals_shots_penalties_faceoffs.gameID = specialGoals.gameID and
                                                                      assist_goals_shots_penalties_faceoffs.teamID = specialGoals.teamID and
                                                                      assist_goals_shots_penalties_faceoffs.playerID = specialGoals.playerID
                                         ) assist_goals_shots_penalties_faceoffs_specialgoals
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
                                            ) as specialAssists on assist_goals_shots_penalties_faceoffs_specialgoals.seasonID = specialAssists.seasonID and
                                                                   assist_goals_shots_penalties_faceoffs_specialgoals.gameID = specialAssists.gameID and
                                                                   assist_goals_shots_penalties_faceoffs_specialgoals.teamID = specialAssists.teamID and
                                                                   assist_goals_shots_penalties_faceoffs_specialgoals.playerID = specialAssists.playerID
                                ) assist_goals_shots_penalties_faceoffs_specialgoals_specialassists
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
                               ) as overTimeGoals on assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.seasonID = overTimeGoals.seasonID and
                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.gameID = overTimeGoals.gameID and
                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.teamID = overTimeGoals.teamID and
                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.playerID = overTimeGoals.playerID
                       ) assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals
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
                      ) as overTimeAssists on assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.seasonID = overTimeAssists.seasonID and
                                              assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.gameID = overTimeAssists.gameID and
                                              assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.teamID = overTimeAssists.teamID and
                                              assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.playerID = overTimeAssists.playerID
              ) assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists
         full outer join
              (
                  select box_scores.*,
                         s.seasonID,
                         s.gameType
                  from box_scores
                  inner join schedules s on s.gameID = box_scores.gameID
              ) boxscores on assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.seasonID = boxscores.seasonID and
                             assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.gameID = boxscores.gameID and
                             assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.teamID = boxscores.teamID and
                             assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.playerID = boxscores.playerID
) players

































