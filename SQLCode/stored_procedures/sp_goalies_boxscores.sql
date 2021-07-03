CREATE procedure goalies_boxscores as
drop table production.dbo.goalies_boxscores
select seasonID,
       gameID,
       teamID,
       playerID,
       GP,
       G,
       SA,
       S,
       W,
       L,
       T,
       TOI,
       SO,
       ROW_NUMBER() over (partition by playerID, gameType order by gameDate desc) as 'gameNumber'
into production.dbo.goalies_boxscores
from (
         select COALESCE(GOALS_SHOTS_WINSLOSSES.seasonID, TOI.seasonID, -1)   as 'seasonID',
                COALESCE(GOALS_SHOTS_WINSLOSSES.gameID, TOI.gameID, -1)       as 'gameID',
                COALESCE(GOALS_SHOTS_WINSLOSSES.teamID, TOI.teamID, -1)       as 'teamID',
                COALESCE(GOALS_SHOTS_WINSLOSSES.playerID, TOI.playerID, -1)   as 'playerID',
                1                                                             as 'GP',  -- games played
                GOALS_SHOTS_WINSLOSSES.G,                                               -- goals
                GOALS_SHOTS_WINSLOSSES.G + GOALS_SHOTS_WINSLOSSES.S           as 'SA',  -- shots against
                GOALS_SHOTS_WINSLOSSES.S,                                               -- shots
                GOALS_SHOTS_WINSLOSSES.W,                                               -- wins
                GOALS_SHOTS_WINSLOSSES.L,                                               -- losses
                GOALS_SHOTS_WINSLOSSES.T,                                               -- ties
                TOI.timeOnIce                                                 as 'TOI', -- time on ice
                IIF(GOALS_SHOTS_WINSLOSSES.G = 0, 1, 0)                       as 'SO',  -- shutouts
                COALESCE(GOALS_SHOTS_WINSLOSSES.gameDate, TOI.gameDate, NULL) as 'gameDate',
                COALESCE(GOALS_SHOTS_WINSLOSSES.gameType, TOI.gameType, NULL) as 'gameType'
         from (
                  select COALESCE(GOALS_SHOTS.seasonID, winsLosses.seasonID)       as 'seasonID',
                         COALESCE(GOALS_SHOTS.gameID, winsLosses.gameID)           as 'gameID',
                         GOALS_SHOTS.teamID,
                         GOALS_SHOTS.playerID,
                         GOALS_SHOTS.G,
                         GOALS_SHOTS.S,
                         case
                             when winsLosses.winner = GOALS_SHOTS.teamID and ISNULL(winsLosses.winner, -1) <> -1
                                 then 'W'
                             else NULL
                             end                                                   as 'W',
                         case
                             when winsLosses.winner <> GOALS_SHOTS.teamID and ISNULL(winsLosses.winner, -1) <> -1
                                 then 'L'
                             else NULL
                             end                                                   as 'L',
                         case
                             when ISNULL(winsLosses.winner, -1) = -1 then 'T'
                             else NULL
                             end                                                   as 'T',
                         COALESCE(GOALS_SHOTS.gameDate, winsLosses.gameDate, NULL) as 'gameDate',
                         COALESCE(GOALS_SHOTS.gameType, winsLosses.gameType, NULL) as 'gameType'
                  from (
                           select COALESCE(GOALS.seasonID, SHOTS.seasonID, -1)   as 'seasonID',
                                  COALESCE(GOALS.gameID, SHOTS.gameID, -1)       as 'gameID',
                                  COALESCE(GOALS.teamID, SHOTS.teamID, -1)       as 'teamID',
                                  COALESCE(GOALS.playerID, SHOTS.playerID, -1)   as 'playerID',
                                  ISNULL(GOALS.numGoals, 0)                      as 'G',
                                  ISNULL(SHOTS.numShots, 0)                      as 'S',
                                  COALESCE(GOALS.gameDate, SHOTS.gameDate, NULL) as 'gameDate',
                                  COALESCE(GOALS.gameType, SHOTS.gameType, NULL) as 'gameType'
                           from (
                                    -- Number of Goals on a goalie by team, player, and game
                                    select s.seasonID,
                                           lf.gameID,
                                           IIF(lf.teamID = s.homeTeamID, s.awayTeamID, s.homeTeamID) as 'teamID',
                                           lf.playerID,
                                           count(*)                                                  as 'numGoals',
                                           s.gameDate,
                                           s.gameType
                                    from live_feed lf
                                             inner join schedules s on lf.gameID = s.gameID
                                    where eventTypeID = 'GOAL'
                                      and playerType = 'GOALIE'
                                    group by lf.teamID, lf.playerID, lf.gameID, s.seasonID, s.awayTeamID, s.homeTeamID,
                                             s.gameDate, s.gameType
                                ) GOALS
                                    full outer join
                                (
                                    -- Number of shots faced by a goalie by team, player, and game
                                    select s.seasonID,
                                           lf.gameID,
                                           IIF(lf.teamID = s.homeTeamID, s.awayTeamID, s.homeTeamID) as 'teamID',
                                           lf.playerID,
                                           count(*)                                                  as 'numShots',
                                           s.gameDate,
                                           s.gameType
                                    from live_feed lf
                                             inner join schedules s on lf.gameID = s.gameID
                                    where eventTypeID = 'SHOT'
                                      and playerType = 'GOALIE'
                                    group by lf.teamID, lf.playerID, lf.gameID, s.seasonID, s.homeTeamID, s.awayTeamID,
                                             s.gameDate, s.gameType
                                ) SHOTS on GOALS.seasonID = SHOTS.seasonID and
                                           GOALS.gameID = SHOTS.gameID and
                                           GOALS.teamID = SHOTS.teamID and
                                           GOALS.playerID = SHOTS.playerID
                       ) GOALS_SHOTS
                           full outer join
                       (
                           -- Individual Game winning team
                           select homeTeam.seasonID,
                                  homeTeam.gameID,
                                  homeTeam.homeTeamID,
                                  ISNULL(homeTeam.homeTeamGoals, 0) as 'homeTeamGoals',
                                  awayTeam.awayTeamID,
                                  ISNULL(awayTeam.awayTeamGoals, 0) as 'awayTeamGoals',
                                  IIF(ISNULL(homeTeam.homeTeamGoals, 0) > ISNULL(awayTeam.awayTeamGoals, 0),
                                      homeTeam.homeTeamID,
                                      IIF(ISNULL(homeTeam.homeTeamGoals, 0) < ISNULL(awayTeam.awayTeamGoals, 0),
                                          awayTeam.awayTeamID,
                                          NULL))                    as 'winner',
                                  homeTeam.gameDate,
                                  homeTeam.gameType
                           from (
                                    select s.seasonID,
                                           s.gameID,
                                           s.homeTeamID,
                                           ISNULL(homeTeamGoals.numGoals, 0) as 'homeTeamGoals',
                                           s.gameDate,
                                           s.gameType
                                    from schedules s
                                             left join
                                         (
                                             select count(*) as 'numGoals',
                                                    live_feed.gameID,
                                                    live_feed.teamID
                                             from live_feed
                                             where eventTypeID = 'GOAL'
                                               and eventSubID = 0
                                             group by gameID, teamID
                                         ) homeTeamGoals on s.gameID = homeTeamGoals.gameID and
                                                            s.homeTeamID = homeTeamGoals.teamID
                                ) homeTeam
                                    inner join
                                (
                                    select s.seasonID,
                                           s.gameID,
                                           s.awayTeamID,
                                           ISNULL(awayTeamGoals.numGoals, 0) as 'awayTeamGoals',
                                           s.gameDate,
                                           s.gameType
                                    from schedules s
                                             left join
                                         (
                                             select count(*) as 'numGoals',
                                                    live_feed.gameID,
                                                    live_feed.teamID
                                             from live_feed
                                             where eventTypeID = 'GOAL'
                                               and eventSubID = 0
                                             group by gameID, teamID
                                         ) awayTeamGoals on s.gameID = awayTeamGoals.gameID and
                                                            s.awayTeamID = awayTeamGoals.teamID
                                ) awayTeam on homeTeam.seasonID = awayTeam.seasonID and
                                              homeTeam.gameID = awayTeam.gameID
                       ) winsLosses
                       on GOALS_SHOTS.seasonID = winsLosses.seasonID and
                          GOALS_SHOTS.gameID = winsLosses.gameID
              ) GOALS_SHOTS_WINSLOSSES
                  full outer join
              (
                  -- time on ice by season, game, team and player
                  select s.gameID,
                         s.seasonID,
                         bs.teamID,
                         bs.playerID,
                         bs.timeOnIce,
                         s.gameDate,
                         s.gameType
                  from box_scores bs
                           inner join schedules s on bs.gameID = s.gameID
                  where timeOnIce is not null
              ) TOI on GOALS_SHOTS_WINSLOSSES.seasonID = TOI.seasonID and
                       GOALS_SHOTS_WINSLOSSES.gameID = TOI.gameID and
                       GOALS_SHOTS_WINSLOSSES.teamID = TOI.teamID and
                       GOALS_SHOTS_WINSLOSSES.playerID = TOI.playerID
         where GOALS_SHOTS_WINSLOSSES.playerID in
               (
                   select pp.playerID
                   from players
                            inner join plays_position pp on players.playerID = pp.playerID
                   where pp.primaryPositionCode = 'G'
               )
     ) inPBI
--      ) goalieBoxscores
-- inner join
--     (

--     ) goalies on goalieBoxscores.playerID = goalies.playerID
-- where goalies.playerID=8476945 order by goalieBoxscores.gameID


select * from goalies_boxscores where playerID=8476945
go

