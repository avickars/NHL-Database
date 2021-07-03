-- drop view if exists game_sheet_skaters;
-- create view game_sheet_skaters as
CREATE procedure skater_game_data as
drop table production.dbo.game_sheet_skaters
select players.seasonID,
       players.gameID,
       players.gameType,
       teamID,
       players.playerID,
       G, -- goals
       A, -- assists
       G + A as 'P', -- points
       S, -- shots
--        CONVERT(float, G) / NULLIF(CONVERT(float, S),0) as 'S%', -- shot percentage
       PIM, -- penalty minutes
       FOW, -- face off wins
       FOL, -- face off losses
--        CONVERT(float, FOW) / NULLIF((CONVERT(float, FOW) + CONVERT(float, FOL)),0) as 'FO%', -- face off percentage
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
       [+/-], -- plus/minus
       1 as 'GP',
       ROW_NUMBER() over (partition by playerID, gameType order by gameDate desc) as 'gameNumber',
       GA,-- give aways
       T, -- takeaways,
       H -- number of hits
into production.dbo.game_sheet_skaters
from
     (
         select COALESCE(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.seasonID,
                                 hits.seasonID, -1)                                                                                                      as 'seasonID',
                         COALESCE(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.gameID,
                                 hits.gameID,
                                 -1)                                                                                                                          as 'gameID',
                         COALESCE(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.gameType,
                                 hits.gameType,
                                 'N/A')                                                                                                                       as 'gameType',
                         COALESCE(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.teamID,
                                 hits.teamID,
                                 -1)                                                                                                                          as 'teamID',
                         COALESCE(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.playerID,
                                 hits.playerID,
                                 -1)                                                                                                                          as 'playerID',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.G,
                                 0)                                                                                                                           as 'G',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.A,
                                 0)                                                                                                                           as 'A',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.S,
                                 0)                                                                                                                           as 'S',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.PIM,
                                 0)                                                                                                                           as 'PIM',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.FOW,
                                 0)                                                                                                                           as 'FOW',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.FOL,
                                 0)                                                                                                                           as 'FOL',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.ESG,
                                 0)                                                                                                                           as 'ESG',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.PPG,
                                 0)                                                                                                                           as 'PPG',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.SHG,
                                 0)                                                                                                                           as 'SHG',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.ESA,
                                 0)                                                                                                                           as 'ESA',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.PPA,
                                 0)                                                                                                                           as 'PPA',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.SHA,
                                 0)                                                                                                                           as 'SHA',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.OTG,
                                 0)                                                                                                                           as 'OTG',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.OTA,
                                 0)                                                                                                                           as 'OTA',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.Number,
                                 -1)                                                                                                                          as 'Number',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.TOI,
                                 'N/A')                                                                                                                       as 'TOI',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.PPTOI,
                                 'N/A')                                                                                                                       as 'PPTOI',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.SHTOI,
                                 'N/A')                                                                                                                       as 'SHTOI',
                         assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.[Status Unknown] as 'Status Unknown',
                         assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.scratched        as 'Scratched',
                         assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.[+/-]            as '+/-',
                         COALESCE(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.gameDate,
                                 hits.gameDate,
                                 NULL)                                                                                                                        as 'gameDate',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.GA,
                                 0)                                                                                                                           as 'GA',
                         ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.T, 0)      as 'T'     ,
                         ISNULL(hits.numHits, 0) as 'H'
         from (
                  select COALESCE(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.seasonID,
                                 takeaways.seasonID, -1)                                                                                                      as 'seasonID',
                         COALESCE(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.gameID,
                                 takeaways.gameID,
                                 -1)                                                                                                                          as 'gameID',
                         COALESCE(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.gameType,
                                 takeaways.gameType,
                                 'N/A')                                                                                                                       as 'gameType',
                         COALESCE(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.teamID,
                                 takeaways.teamID,
                                 -1)                                                                                                                          as 'teamID',
                         COALESCE(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.playerID,
                                 takeaways.playerID,
                                 -1)                                                                                                                          as 'playerID',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.G,
                                 0)                                                                                                                           as 'G',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.A,
                                 0)                                                                                                                           as 'A',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.S,
                                 0)                                                                                                                           as 'S',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.PIM,
                                 0)                                                                                                                           as 'PIM',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.FOW,
                                 0)                                                                                                                           as 'FOW',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.FOL,
                                 0)                                                                                                                           as 'FOL',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.ESG,
                                 0)                                                                                                                           as 'ESG',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.PPG,
                                 0)                                                                                                                           as 'PPG',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.SHG,
                                 0)                                                                                                                           as 'SHG',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.ESA,
                                 0)                                                                                                                           as 'ESA',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.PPA,
                                 0)                                                                                                                           as 'PPA',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.SHA,
                                 0)                                                                                                                           as 'SHA',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.OTG,
                                 0)                                                                                                                           as 'OTG',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.OTA,
                                 0)                                                                                                                           as 'OTA',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.Number,
                                 -1)                                                                                                                          as 'Number',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.TOI,
                                 'N/A')                                                                                                                       as 'TOI',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.PPTOI,
                                 'N/A')                                                                                                                       as 'PPTOI',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.SHTOI,
                                 'N/A')                                                                                                                       as 'SHTOI',
                         assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.[Status Unknown] as 'Status Unknown',
                         assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.scratched        as 'Scratched',
                         assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.[+/-]            as '+/-',
                         COALESCE(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.gameDate,
                                 takeaways.gameDate,
                                 NULL)                                                                                                                        as 'gameDate',
                         ISNULL(
                                 assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.GA,
                                 0)                                                                                                                           as 'GA',
                         ISNULL(takeaways.numTakeaways, 0)                                                                                                    as 'T'
                  from (
                           select COALESCE(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.seasonID,
                                          giveaways.seasonID, -1)                                                                                            as 'seasonID',
                                  COALESCE(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.gameID,
                                          giveaways.gameID,
                                          -1)                                                                                                                as 'gameID',
                                  COALESCE(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.gameType,
                                          giveaways.gameType,
                                          'N/A')                                                                                                             as 'gameType',
                                  COALESCE(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.teamID,
                                          giveaways.teamID,
                                          -1)                                                                                                                as 'teamID',
                                  COALESCE(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.playerID,
                                          giveaways.playerID,
                                          -1)                                                                                                                as 'playerID',
                                  ISNULL(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.G,
                                          0)                                                                                                                 as 'G',
                                  ISNULL(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.A,
                                          0)                                                                                                                 as 'A',
                                  ISNULL(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.S,
                                          0)                                                                                                                 as 'S',
                                  ISNULL(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.PIM,
                                          0)                                                                                                                 as 'PIM',
                                  ISNULL(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.FOW,
                                          0)                                                                                                                 as 'FOW',
                                  ISNULL(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.FOL,
                                          0)                                                                                                                 as 'FOL',
                                  ISNULL(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.ESG,
                                          0)                                                                                                                 as 'ESG',
                                  ISNULL(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.PPG,
                                          0)                                                                                                                 as 'PPG',
                                  ISNULL(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.SHG,
                                          0)                                                                                                                 as 'SHG',
                                  ISNULL(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.ESA,
                                          0)                                                                                                                 as 'ESA',
                                  ISNULL(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.PPA,
                                          0)                                                                                                                 as 'PPA',
                                  ISNULL(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.SHA,
                                          0)                                                                                                                 as 'SHA',
                                  ISNULL(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.OTG,
                                          0)                                                                                                                 as 'OTG',
                                  ISNULL(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.OTA,
                                          0)                                                                                                                 as 'OTA',
                                  ISNULL(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.Number,
                                          -1)                                                                                                                as 'Number',
                                  ISNULL(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.TOI,
                                          'N/A')                                                                                                             as 'TOI',
                                  ISNULL(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.PPTOI,
                                          'N/A')                                                                                                             as 'PPTOI',
                                  ISNULL(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.SHTOI,
                                          'N/A')                                                                                                             as 'SHTOI',
                                  assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.[Status Unknown] as 'Status Unknown',
                                  assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.scratched        as 'Scratched',
                                  assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.[+/-]            as '+/-',
                                  COALESCE(
                                          assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.gameDate,
                                          giveaways.gameDate,
                                          NULL)                                                                                                              as 'gameDate',
                                  ISNULL(giveaways.numGiveaways, 0)                                                                                          as 'GA'
                           from (
                                    select COALESCE(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.seasonID,
                                                   boxscores.seasonID, -1)               as 'seasonID',
                                           COALESCE(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.gameID,
                                                   boxscores.gameID, -1)                 as 'gameID',
                                           COALESCE(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.gameType,
                                                   boxscores.gameType, 'N/A')            as 'gameType',
                                           COALESCE(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.teamID,
                                                   boxscores.teamID, -1)                 as 'teamID',
                                           COALESCE(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.playerID,
                                                   boxscores.playerID, -1)               as 'playerID',
                                           ISNULL(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.G,
                                                   0)                                    as 'G',
                                           ISNULL(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.A,
                                                   0)                                    as 'A',
                                           ISNULL(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.S,
                                                   0)                                    as 'S',
                                           ISNULL(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.PIM,
                                                   0)                                    as 'PIM',
                                           ISNULL(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.FOW,
                                                   0)                                    as 'FOW',
                                           ISNULL(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.FOL,
                                                   0)                                    as 'FOL',
                                           ISNULL(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.ESG,
                                                   0)                                    as 'ESG',
                                           ISNULL(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.PPG,
                                                   0)                                    as 'PPG',
                                           ISNULL(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.SHG,
                                                   0)                                    as 'SHG',
                                           ISNULL(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.ESA,
                                                   0)                                    as 'ESA',
                                           ISNULL(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.PPA,
                                                   0)                                    as 'PPA',
                                           ISNULL(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.SHA,
                                                   0)                                    as 'SHA',
                                           ISNULL(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.OTG,
                                                   0)                                    as 'OTG',
                                           ISNULL(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.OTA,
                                                   0)                                    as 'OTA',
                                           ISNULL(boxscores.jerseyNumber, -1)            as 'Number',
                                           ISNULL(boxscores.timeOnIce, 'N/A')            as 'TOI',
                                           ISNULL(boxscores.powerPlayTimeOnIce, 'N/A')   as 'PPTOI',
                                           ISNULL(boxscores.shortHandedTimeOnIce, 'N/A') as 'SHTOI',
                                           boxscores.unknown                             as 'Status Unknown',
                                           boxscores.scratched                           as 'Scratched',
                                           boxscores.plusMinus                           as '+/-',
                                           COALESCE(
                                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.gameDate,
                                                   boxscores.gameDate, NULL)             as 'gameDate'
                                    from (
                                             select COALESCE(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.seasonID,
                                                            overTimeAssists.seasonID, -1)    as 'seasonID',
                                                    COALESCE(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.gameID,
                                                            overTimeAssists.gameID, -1)      as 'gameID',
                                                    COALESCE(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.gameType,
                                                            overTimeAssists.gameType, 'N/A') as 'gameType',
                                                    COALESCE(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.teamID,
                                                            overTimeAssists.teamID, -1)      as 'teamID',
                                                    COALESCE(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.playerID,
                                                            overTimeAssists.playerID, -1)    as 'playerID',
                                                    ISNULL(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.G,
                                                            0)                               as 'G',
                                                    ISNULL(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.A,
                                                            0)                               as 'A',
                                                    ISNULL(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.S,
                                                            0)                               as 'S',
                                                    ISNULL(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.PIM,
                                                            0)                               as 'PIM',
                                                    ISNULL(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.FOW,
                                                            0)                               as 'FOW',
                                                    ISNULL(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.FOL,
                                                            0)                               as 'FOL',
                                                    ISNULL(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.ESG,
                                                            0)                               as 'ESG',
                                                    ISNULL(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.PPG,
                                                            0)                               as 'PPG',
                                                    ISNULL(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.SHG,
                                                            0)                               as 'SHG',
                                                    ISNULL(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.ESA,
                                                            0)                               as 'ESA',
                                                    ISNULL(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.PPA,
                                                            0)                               as 'PPA',
                                                    ISNULL(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.SHA,
                                                            0)                               as 'SHA',
                                                    ISNULL(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.OTG,
                                                            0)                               as 'OTG',
                                                    ISNULL(overTimeAssists.OTA, 0)           as 'OTA',
                                                    COALESCE(
                                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.gameDate,
                                                            overTimeAssists.gameDate, NULL)  as 'gameDate'

                                             from (
                                                      -- selecting all the assists, goals, shots, penalty mins ,special goals, special assists, overtime goals and overtime assists by playerID,gameID, seasonID and teamID
                                                      select COALESCE(
                                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.seasonID,
                                                                     overTimeGoals.seasonID, -1)    as 'seasonID',
                                                             COALESCE(
                                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.gameID,
                                                                     overTimeGoals.gameID, -1)      as 'gameID',
                                                             COALESCE(
                                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.gameType,
                                                                     overTimeGoals.gameType, 'N/A') as 'gameType',
                                                             COALESCE(
                                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.teamID,
                                                                     overTimeGoals.teamID, -1)      as 'teamID',
                                                             COALESCE(
                                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.playerID,
                                                                     overTimeGoals.playerID, -1)    as 'playerID',
                                                             ISNULL(
                                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.G,
                                                                     0)                             as 'G',
                                                             ISNULL(
                                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.A,
                                                                     0)                             as 'A',
                                                             ISNULL(
                                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.S,
                                                                     0)                             as 'S',
                                                             ISNULL(
                                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.PIM,
                                                                     0)                             as 'PIM',
                                                             ISNULL(
                                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.FOW,
                                                                     0)                             as 'FOW',
                                                             ISNULL(
                                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.FOL,
                                                                     0)                             as 'FOL',
                                                             ISNULL(
                                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.ESG,
                                                                     0)                             as 'ESG',
                                                             ISNULL(
                                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.PPG,
                                                                     0)                             as 'PPG',
                                                             ISNULL(
                                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.SHG,
                                                                     0)                             as 'SHG',
                                                             ISNULL(
                                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.ESA,
                                                                     0)                             as 'ESA',
                                                             ISNULL(
                                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.PPA,
                                                                     0)                             as 'PPA',
                                                             ISNULL(
                                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.SHA,
                                                                     0)                             as 'SHA',
                                                             ISNULL(overTimeGoals.OTG, 0)           as 'OTG',
                                                             COALESCE(
                                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.gameDate,
                                                                     overTimeGoals.gameDate, NULL)  as 'gameDate'
                                                      from (
                                                               -- selecting all the assists, goals, shots, penalty mins ,special goals, special assists and overtime goals by playerID,gameID, seasonID and teamID
                                                               select COALESCE(
                                                                              assist_goals_shots_penalties_faceoffs_specialgoals.seasonID,
                                                                              specialAssists.seasonID,
                                                                              -1)                                                       as 'seasonID',
                                                                      COALESCE(
                                                                              assist_goals_shots_penalties_faceoffs_specialgoals.gameID,
                                                                              specialAssists.gameID,
                                                                              -1)                                                       as 'gameID',
                                                                      COALESCE(
                                                                              assist_goals_shots_penalties_faceoffs_specialgoals.gameType,
                                                                              specialAssists.gameType,
                                                                              'N/A')                                                    as 'gameType',
                                                                      COALESCE(
                                                                              assist_goals_shots_penalties_faceoffs_specialgoals.teamID,
                                                                              specialAssists.teamID,
                                                                              -1)                                                       as 'teamID',
                                                                      COALESCE(
                                                                              assist_goals_shots_penalties_faceoffs_specialgoals.playerID,
                                                                              specialAssists.playerID,
                                                                              -1)                                                       as 'playerID',
                                                                      ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals.G, 0)   as 'G',
                                                                      ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals.A, 0)   as 'A',
                                                                      ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals.S, 0)   as 'S',
                                                                      ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals.PIM, 0) as 'PIM',
                                                                      ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals.FOW, 0) as 'FOW',
                                                                      ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals.FOL, 0) as 'FOL',
                                                                      ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals.ESG, 0) as 'ESG',
                                                                      ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals.PPG, 0) as 'PPG',
                                                                      ISNULL(assist_goals_shots_penalties_faceoffs_specialgoals.SHG, 0) as 'SHG',
                                                                      ISNULL(specialAssists.ESA, 0)                                     as 'ESA',
                                                                      ISNULL(specialAssists.PPA, 0)                                     as 'PPA',
                                                                      ISNULL(specialAssists.SHA, 0)                                     as 'SHA',
                                                                      COALESCE(
                                                                              assist_goals_shots_penalties_faceoffs_specialgoals.gameDate,
                                                                              specialAssists.gameDate,
                                                                              NULL)                                                     as 'gameDate'

                                                               from (
                                                                        -- selecting all the assists, goals, shots, penalty mins ,special goals and special assists by playerID,gameID, seasonID and teamID
                                                                        select COALESCE(
                                                                                       assist_goals_shots_penalties_faceoffs.seasonID,
                                                                                       specialGoals.seasonID,
                                                                                       -1)                                          as 'seasonID',
                                                                               COALESCE(
                                                                                       assist_goals_shots_penalties_faceoffs.gameID,
                                                                                       specialGoals.gameID,
                                                                                       -1)                                          as 'gameID',
                                                                               COALESCE(
                                                                                       assist_goals_shots_penalties_faceoffs.gameType,
                                                                                       specialGoals.gameType,
                                                                                       'N/A')                                       as 'gameType',
                                                                               COALESCE(
                                                                                       assist_goals_shots_penalties_faceoffs.teamID,
                                                                                       specialGoals.teamID,
                                                                                       -1)                                          as 'teamID',
                                                                               COALESCE(
                                                                                       assist_goals_shots_penalties_faceoffs.playerID,
                                                                                       specialGoals.playerID,
                                                                                       -1)                                          as 'playerID',
                                                                               ISNULL(assist_goals_shots_penalties_faceoffs.G, 0)   as 'G',
                                                                               ISNULL(assist_goals_shots_penalties_faceoffs.A, 0)   as 'A',
                                                                               ISNULL(assist_goals_shots_penalties_faceoffs.S, 0)   as 'S',
                                                                               ISNULL(assist_goals_shots_penalties_faceoffs.PIM, 0) as 'PIM',
                                                                               ISNULL(assist_goals_shots_penalties_faceoffs.FOW, 0) as 'FOW',
                                                                               ISNULL(assist_goals_shots_penalties_faceoffs.FOL, 0) as 'FOL',
                                                                               ISNULL(specialGoals.ESG, 0)                          as 'ESG',
                                                                               ISNULL(specialGoals.PPG, 0)                          as 'PPG',
                                                                               ISNULL(specialGoals.SHG, 0)                          as 'SHG',
                                                                               COALESCE(
                                                                                       assist_goals_shots_penalties_faceoffs.gameDate,
                                                                                       specialGoals.gameDate,
                                                                                       NULL)                                        as 'gameDate'
                                                                        from (
                                                                                 -- selecting all the assists, goals, shots, penalty mins and special goals by playerID,gameID, seasonID and teamID
                                                                                 select COALESCE(
                                                                                                assist_goals_shots_penalties.seasonID,
                                                                                                faceOffs.seasonID,
                                                                                                -1)                                                        as 'seasonID',
                                                                                        COALESCE(assist_goals_shots_penalties.gameID, faceOffs.gameID, -1) as 'gameID',
                                                                                        COALESCE(
                                                                                                assist_goals_shots_penalties.gameType,
                                                                                                faceOffs.gameType,
                                                                                                'N/A')                                                     as 'gameType',
                                                                                        COALESCE(assist_goals_shots_penalties.teamID, faceOffs.teamID, -1) as 'teamID',
                                                                                        COALESCE(
                                                                                                assist_goals_shots_penalties.playerID,
                                                                                                faceOffs.playerID,
                                                                                                -1)                                                        as 'playerID',
                                                                                        ISNULL(assist_goals_shots_penalties.G, 0)                          as 'G',
                                                                                        ISNULL(assist_goals_shots_penalties.A, 0)                          as 'A',
                                                                                        ISNULL(assist_goals_shots_penalties.S, 0)                          as 'S',
                                                                                        ISNULL(assist_goals_shots_penalties.PIM, 0)                        as 'PIM',
                                                                                        ISNULL(faceOffs.numWins, 0)                                        as 'FOW',
                                                                                        ISNULL(faceOffs.numLosses, 0)                                      as 'FOL',
                                                                                        COALESCE(
                                                                                                assist_goals_shots_penalties.gameDate,
                                                                                                faceOffs.gameDate,
                                                                                                NULL)                                                      as 'gameDate'
                                                                                 from (
                                                                                          -- selecting all the assists, goals, shots and penalty mins by playerID,gameID, seasonID and teamID
                                                                                          select COALESCE(assist_goals_shots.seasonID, penalties.seasonID, -1)    as 'seasonID',
                                                                                                 COALESCE(assist_goals_shots.gameID, penalties.gameID, -1)        as 'gameID',
                                                                                                 COALESCE(assist_goals_shots.gameType, penalties.gameType, 'N/A') as 'gameType',
                                                                                                 COALESCE(assist_goals_shots.teamID, penalties.teamID, -1)        as 'teamID',
                                                                                                 COALESCE(assist_goals_shots.playerID, penalties.playerID, -1)    as 'playerID',
                                                                                                 ISNULL(assist_goals_shots.G, 0)                                  as 'G',
                                                                                                 ISNULL(assist_goals_shots.A, 0)                                  as 'A',
                                                                                                 ISNULL(assist_goals_shots.S, 0)                                  as 'S',
                                                                                                 ISNULL(penalties.PIM, 0)                                         as 'PIM',
                                                                                                 COALESCE(assist_goals_shots.gameDate, penalties.gameDate, NULL)  as 'gameDate'
                                                                                          from (
                                                                                                   -- selecting all the assists, goals and shots by playerID,gameID, seasonID and teamID
                                                                                                   select COALESCE(assists_goals.seasonID, shots.seasonID, -1)    as 'seasonID',
                                                                                                          COALESCE(assists_goals.gameID, shots.gameID, -1)        as 'gameID',
                                                                                                          COALESCE(assists_goals.gameType, shots.gameType, 'N/A') as 'gameType',
                                                                                                          COALESCE(assists_goals.teamID, shots.teamID, -1)        as 'teamID',
                                                                                                          COALESCE(assists_goals.playerID, shots.playerID, -1)    as 'playerID',
                                                                                                          ISNULL(assists_goals.G, 0)                              as 'G',
                                                                                                          ISNULL(assists_goals.A, 0)                              as 'A',
                                                                                                          ISNULL(shots.shots, 0)                                  as 'S',
                                                                                                          COALESCE(assists_goals.gameDate, shots.gameDate, NULL)  as 'gameDate'
                                                                                                   from (
                                                                                                            -- selecting all the assists and goals by playerID,gameID, seasonID and teamID
                                                                                                            select COALESCE(assists.seasonID, goals.seasonID, -1)    as 'seasonID',
                                                                                                                   COALESCE(assists.gameID, goals.gameID, -1)        as 'gameID',
                                                                                                                   COALESCE(assists.gameType, goals.gameType, 'N/A') as 'gameType',
                                                                                                                   COALESCE(assists.teamID, goals.teamID, -1)        as 'teamID',
                                                                                                                   COALESCE(assists.playerID, goals.playerID, -1)    as 'playerID',
                                                                                                                   ISNULL(goals.goals, 0)                            as 'G',
                                                                                                                   ISNULL(assists.assists, 0)                        as 'A',
                                                                                                                   COALESCE(assists.gameDate, goals.gameDate, NULL)  as 'gameDate'
                                                                                                            from (
                                                                                                                     -- selecting all the assists by playerID,gameID, seasonID and teamID
                                                                                                                     select lf.playerID,
                                                                                                                            s.gameType,
                                                                                                                            lf.gameID,
                                                                                                                            s.seasonID,
                                                                                                                            count(*) as 'assists',
                                                                                                                            lf.teamID,
                                                                                                                            s.gameDate
                                                                                                                     from live_feed lf
                                                                                                                              inner join schedules s on s.gameID = lf.gameID
                                                                                                                     where lf.eventTypeID = 'GOAL'
                                                                                                                       and lf.playerType = 'Assist'
                                                                                                                     group by lf.playerID,
                                                                                                                              lf.gameID,
                                                                                                                              s.gameType,
                                                                                                                              s.seasonID,
                                                                                                                              lf.teamID,
                                                                                                                              s.gameDate
                                                                                                                 ) assists
                                                                                                                     full outer join
                                                                                                                 (
                                                                                                                     -- selecting all the goals by playerID,gameID, seasonID and teamID
                                                                                                                     select lf.playerID,
                                                                                                                            s.gameType,
                                                                                                                            lf.gameID,
                                                                                                                            s.seasonID,
                                                                                                                            count(*) as 'goals',
                                                                                                                            lf.teamID,
                                                                                                                            s.gameDate
                                                                                                                     from live_feed lf
                                                                                                                              inner join schedules s on s.gameID = lf.gameID
                                                                                                                     where lf.eventTypeID = 'GOAL'
                                                                                                                       and lf.playerType = 'Scorer'
                                                                                                                     group by lf.playerID,
                                                                                                                              lf.gameID,
                                                                                                                              s.gameType,
                                                                                                                              s.seasonID,
                                                                                                                              lf.teamID,
                                                                                                                              s.gameDate
                                                                                                                 ) goals
                                                                                                                 on assists.seasonID = goals.seasonID and
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
                                                                                                                   lf.teamID,
                                                                                                                   s.gameDate
                                                                                                            from live_feed lf
                                                                                                                     inner join schedules s on lf.gameID = s.gameID
                                                                                                            where lf.eventTypeID = 'SHOT'
                                                                                                              and lf.playerType = 'Shooter'
                                                                                                            group by lf.playerID,
                                                                                                                     lf.gameID,
                                                                                                                     s.gameType,
                                                                                                                     s.seasonID,
                                                                                                                     lf.teamID,
                                                                                                                     s.gameDate
                                                                                                        ) shots
                                                                                                        on assists_goals.seasonID = shots.seasonID and
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
                                                                                                          lf.teamID,
                                                                                                          s.gameDate
                                                                                                   from live_feed lf
                                                                                                            inner join schedules s on lf.gameID = s.gameID
                                                                                                   where lf.eventTypeID = 'PENALTY'
                                                                                                     and lf.playerType = 'PenaltyOn'
                                                                                                   group by lf.playerID,
                                                                                                            lf.gameID,
                                                                                                            s.gameType,
                                                                                                            s.seasonID,
                                                                                                            lf.teamID,
                                                                                                            s.gameDate
                                                                                               ) penalties
                                                                                               on assist_goals_shots.seasonID = penalties.seasonID and
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
                                                                                                 isnull(Loser, 0)  as 'numLosses',
                                                                                                 isnull(Winner, 0) as 'numWins',
                                                                                                 gameDate
                                                                                          from (
                                                                                                   -- Number of face-off wins/losses by player, and game, and team
                                                                                                   select s.seasonID,
                                                                                                          s.gameID,
                                                                                                          IIF(
                                                                                                                  lf.playerType = 'Winner',
                                                                                                                  lf.teamID,
                                                                                                                  IIF(lf.teamID = s.homeTeamID, s.awayTeamID, s.homeTeamID)) as 'teamID',
                                                                                                          lf.playerID,
                                                                                                          lf.playerType,
                                                                                                          lf.numEvents,
                                                                                                          s.gameType,
                                                                                                          s.gameDate
                                                                                                   from (
                                                                                                            select teamID,
                                                                                                                   gameID,
                                                                                                                   playerType,
                                                                                                                   playerID,
                                                                                                                   count(playerType) as 'numEvents'
                                                                                                            from live_feed
                                                                                                            where eventTypeID = 'FACEOFF'
                                                                                                            group by playerType, playerID, gameID, teamID
                                                                                                        ) lf
                                                                                                            inner join schedules s on lf.gameID = s.gameID
                                                                                               ) as sourceTable
                                                                                                   pivot
                                                                                                   (
                                                                                                   sum(numEvents) for playerType in ("Loser", "Winner")
                                                                                                   ) as pivotTable
                                                                                      ) as faceOffs
                                                                                      on assist_goals_shots_penalties.seasonID = faceOffs.seasonID and
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
                                                                                        ISNULL(PPG, 0)  as 'PPG',
                                                                                        ISNULL(SSH, 0)  as 'SHG',
                                                                                        gameDate
                                                                                 from (
                                                                                          select lf.playerID,
                                                                                                 s.gameType,
                                                                                                 lf.gameID,
                                                                                                 s.seasonID,
                                                                                                 count(*) as 'goals',
                                                                                                 lf.teamID,
                                                                                                 lf.strength,
                                                                                                 s.gameDate
                                                                                          from live_feed lf
                                                                                                   inner join schedules s on s.gameID = lf.gameID
                                                                                          where lf.eventTypeID = 'GOAL'
                                                                                            and lf.playerType = 'Scorer'
                                                                                          group by lf.playerID,
                                                                                                   lf.gameID,
                                                                                                   s.gameType,
                                                                                                   s.seasonID,
                                                                                                   lf.teamID,
                                                                                                   lf.strength,
                                                                                                   s.gameDate
                                                                                      ) as sourceTable
                                                                                          pivot
                                                                                          (
                                                                                          sum(goals) for strength in ("EVEN", "PPG","SSH")
                                                                                          ) as pivotTable
                                                                             ) as specialGoals
                                                                             on assist_goals_shots_penalties_faceoffs.seasonID = specialGoals.seasonID and
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
                                                                               ISNULL(PPG, 0)  as 'PPA',
                                                                               ISNULL(SSH, 0)  as 'SHA',
                                                                               gameDate
                                                                        from (
                                                                                 select lf.playerID,
                                                                                        s.gameType,
                                                                                        lf.gameID,
                                                                                        s.seasonID,
                                                                                        count(*) as 'assists',
                                                                                        lf.teamID,
                                                                                        lf.strength,
                                                                                        s.gameDate
                                                                                 from live_feed lf
                                                                                          inner join schedules s on s.gameID = lf.gameID
                                                                                 where lf.eventTypeID = 'GOAL'
                                                                                   and lf.playerType = 'Assist'
                                                                                 group by lf.playerID, lf.gameID,
                                                                                          s.gameType,
                                                                                          s.seasonID,
                                                                                          lf.teamID, lf.strength,
                                                                                          s.gameDate
                                                                             ) as sourceTable
                                                                                 pivot
                                                                                 (
                                                                                 sum(assists) for strength in ("EVEN", "PPG","SSH")
                                                                                 ) as pivotTable
                                                                    ) as specialAssists
                                                                    on assist_goals_shots_penalties_faceoffs_specialgoals.seasonID =
                                                                       specialAssists.seasonID and
                                                                       assist_goals_shots_penalties_faceoffs_specialgoals.gameID =
                                                                       specialAssists.gameID and
                                                                       assist_goals_shots_penalties_faceoffs_specialgoals.teamID =
                                                                       specialAssists.teamID and
                                                                       assist_goals_shots_penalties_faceoffs_specialgoals.playerID =
                                                                       specialAssists.playerID
                                                           ) assist_goals_shots_penalties_faceoffs_specialgoals_specialassists
                                                               full outer join
                                                           (
                                                               -- getting playoff overtime goals
                                                               select lf.playerID,
                                                                      s.gameType,
                                                                      lf.gameID,
                                                                      s.seasonID,
                                                                      count(*) as 'OTG',
                                                                      lf.teamID,
                                                                      s.gameDate
                                                               from live_feed lf
                                                                        inner join schedules s on s.gameID = lf.gameID
                                                               where lf.eventTypeID = 'GOAL'
                                                                 and lf.playerType = 'Scorer'
                                                                 and lf.periodNum > 3
                                                                 and gameType = 'P'
                                                               group by lf.playerID, lf.gameID, s.gameType, s.seasonID,
                                                                        lf.teamID,
                                                                        periodNum, s.gameDate
                                                               union
                                                               -- Getting regular and preseason season overtime goals
                                                               select lf.playerID,
                                                                      s.gameType,
                                                                      lf.gameID,
                                                                      s.seasonID,
                                                                      count(*) as 'OTG',
                                                                      lf.teamID,
                                                                      s.gameDate
                                                               from live_feed lf
                                                                        inner join schedules s on s.gameID = lf.gameID
                                                               where lf.eventTypeID = 'GOAL'
                                                                 and lf.playerType = 'Scorer'
                                                                 and lf.periodNum = 4
                                                                 and (gameType = 'R' or gameType = 'PR')
                                                               group by lf.playerID, lf.gameID, s.gameType, s.seasonID,
                                                                        lf.teamID,
                                                                        periodNum, s.gameDate
                                                           ) as overTimeGoals
                                                           on assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.seasonID =
                                                              overTimeGoals.seasonID and
                                                              assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.gameID =
                                                              overTimeGoals.gameID and
                                                              assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.teamID =
                                                              overTimeGoals.teamID and
                                                              assist_goals_shots_penalties_faceoffs_specialgoals_specialassists.playerID =
                                                              overTimeGoals.playerID
                                                  ) assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals
                                                      full outer join
                                                  (
                                                      -- getting playoff overtime goals
                                                      select lf.playerID,
                                                             s.gameType,
                                                             lf.gameID,
                                                             s.seasonID,
                                                             count(*) as 'OTA',
                                                             lf.teamID,
                                                             s.gameDate
                                                      from live_feed lf
                                                               inner join schedules s on s.gameID = lf.gameID
                                                      where lf.eventTypeID = 'GOAL'
                                                        and lf.playerType = 'Assist'
                                                        and lf.periodNum > 3
                                                        and gameType = 'P'
                                                      group by lf.playerID, lf.gameID, s.gameType, s.seasonID,
                                                               lf.teamID,
                                                               periodNum,
                                                               s.gameDate
                                                      union
                                                      -- Getting regular and preseason season overtime goals
                                                      select lf.playerID,
                                                             s.gameType,
                                                             lf.gameID,
                                                             s.seasonID,
                                                             count(*) as 'OTA',
                                                             lf.teamID,
                                                             s.gameDate
                                                      from live_feed lf
                                                               inner join schedules s on s.gameID = lf.gameID
                                                      where lf.eventTypeID = 'GOAL'
                                                        and lf.playerType = 'Assist'
                                                        and lf.periodNum = 4
                                                        and (gameType = 'R' or gameType = 'PR')
                                                      group by lf.playerID, lf.gameID, s.gameType, s.seasonID,
                                                               lf.teamID,
                                                               periodNum,
                                                               s.gameDate
                                                  ) as overTimeAssists
                                                  on assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.seasonID =
                                                     overTimeAssists.seasonID and
                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.gameID =
                                                     overTimeAssists.gameID and
                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.teamID =
                                                     overTimeAssists.teamID and
                                                     assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals.playerID =
                                                     overTimeAssists.playerID
                                         ) assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists
                                             full outer join
                                         (
                                             select box_scores.*,
                                                    s.seasonID,
                                                    s.gameType,
                                                    s.gameDate
                                             from box_scores
                                                      inner join schedules s on s.gameID = box_scores.gameID
                                         ) boxscores
                                         on assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.seasonID =
                                            boxscores.seasonID and
                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.gameID =
                                            boxscores.gameID and
                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.teamID =
                                            boxscores.teamID and
                                            assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists.playerID =
                                            boxscores.playerID
                                ) assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores
                                    full outer join
                                (
                                    select count(*) as 'numGiveaways',
                                           lf.playerID,
                                           lf.gameID,
                                           s.gameType,
                                           s.seasonID,
                                           lf.teamID,
                                           s.gameDate
                                    from live_feed lf
                                             inner join schedules s on s.gameID = lf.gameID
                                    where lf.eventTypeID = 'GIVEAWAY'
                                    group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID, s.gameDate
                                ) as giveaways
                                on assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.seasonID =
                                   giveaways.seasonID and
                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.gameID =
                                   giveaways.gameID and
                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.teamID =
                                   giveaways.teamID and
                                   assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores.playerID =
                                   giveaways.playerID
                       ) as assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways
                           full outer join (
                      select count(*) as 'numTakeaways',
                             lf.playerID,
                             lf.gameID,
                             s.gameType,
                             s.seasonID,
                             lf.teamID,
                             s.gameDate
                      from live_feed lf
                               inner join schedules s on s.gameID = lf.gameID
                      where lf.eventTypeID = 'TAKEAWAY'
                      group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID, s.gameDate
                  ) takeaways
                                           on assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.seasonID =
                                              takeaways.seasonID and
                                              assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.gameID =
                                              takeaways.gameID and
                                              assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.teamID =
                                              takeaways.teamID and
                                              assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways.playerID =
                                              takeaways.playerID
              ) as assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways
         full outer join
             (
                select count(*) as 'numHits',
                       lf.playerID,
                       lf.gameID,
                       s.gameType,
                       s.seasonID,
                       lf.teamID,
                       s.gameDate
                from live_feed lf
                inner join schedules s on s.gameID = lf.gameID
                where lf.eventTypeID = 'HIT' and lf.playerType = 'Hitter'
                group by lf.playerID, lf.gameID, s.gameType, s.seasonID, lf.teamID, s.gameDate
            ) hits on assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.seasonID =
                                              hits.seasonID and
                                              assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.gameID =
                                                hits.gameID and
                                              assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.teamID =
                                              hits.teamID and
                                              assist_goals_shots_penalties_faceoffs_specialgoals_specialassists_overtimegoals_overtimeassists_boxscores_giveaways_takeaways.playerID =
                                              hits.playerID


) players
where players.playerID in
         (
             select playerID
             from (
                  select playerID,
                         primaryPositionCode,
                         ROW_NUMBER() over (partition by playerID order by date desc ) as 'rowNum'
                  from plays_position
              ) pos
             where pos.rowNum = 1 and pos.primaryPositionCode <> 'G'
         )
go

