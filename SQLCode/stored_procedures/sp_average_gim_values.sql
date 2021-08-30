CREATE procedure sp_average_gim_values_by_player_view()
begin

drop table if exists stage_hockey.gim_values_per_game;
create table stage_hockey.gim_values_per_game as
select GAMES.seasonID,
       GAMES.gameID,
       GAMES.gameType,
       GAMES.teamID,
       GAMES.playerID,
       IF(GIM.value is null, 0, GIM.value) as 'gimForIndvGame',
       ROW_NUMBER() over (partition by GAMES.seasonID, GAMES.teamID, GAMES.playerID order by GAMES.gameID) as 'gameNumber',
       SUM(IF(GIM.value is null, 0, GIM.value)) over (partition by GAMES.seasonID, GAMES.teamID, GAMES.playerID order by GAMES.gameID) as 'gimCumTotal',
       AVG(IF(GIM.value is null, 0, GIM.value)) over (partition by GAMES.seasonID, GAMES.teamID, GAMES.playerID order by GAMES.gameID) as 'gimMean'
from (
         select s.seasonID,
                bs.gameID,
                bs.playerID,
                bs.teamID,
                s.gameType
         from box_scores bs
                  inner join schedules s on bs.gameID = s.gameID
         where scratched = 0 and
               seasonID >= 20102011 and
               timeOnIce is not null and
               s.gameType in ('R', 'P')
     ) GAMES
left join
    (
        select gim.gameID,
               playerID,
               sum(if(awayTeam = 1, awayProbability, homeProbability)) as 'value'
        from stage_hockey.gim_values gim
        group by gim.gameID, playerID
    ) GIM ON GAMES.gameID =  GIM.gameID and GAMES.playerID = GIM.playerID
order by gameID,playerID;



# Getting each players GIM by season
drop table if exists stage_hockey.gimValuesPerPlayerAndSeason;
create table stage_hockey.gimValuesPerPlayerAndSeason as
select GIM_VALUES.seasonID,
       GIM_VALUES.playerID,
       GIM_VALUES.gameNumber,
       GIM_VALUES.gimMean
from stage_hockey.gim_values_per_game GIM_VALUES
inner join
    (
        # Getting the max game number to use as a filter
        select seasonID,
             playerID,
               max(gameNumber) 'maxGameNumber'
        from stage_hockey.gim_values_per_game GIM_VALUES
        group by seasonID, playerID
    ) MAX_GAM_NUM on GIM_VALUES.seasonID = MAX_GAM_NUM.seasonID and
                     MAX_GAM_NUM.playerID = GIM_VALUES.playerID and
 MAX_GAM_NUM.maxGameNumber = GIM_VALUES.gameNumber;


# Each players position
drop table if exists stage_hockey.current_positions;
create table stage_hockey.current_positions as
select playerID,
    primaryPositionCode
from (
      select playerID,
             primaryPositionCode,
             row_number() over (partition by playerID order by date desc ) as 'ROW_NUM'
      from plays_position
      where primaryPositionCode is not null
  ) POSITION
WHERE POSITION.ROW_NUM = 1;

drop table if exists stage_hockey.average_gim_values_by_player;
create table stage_hockey.average_gim_values_by_player as
select GIM_VALUES.seasonID,
       GIM_VALUES.GAMEID,
       GIM_VALUES.GAMETYPE,
       GIM_VALUES.TEAMID,
       GIM_VALUES.PLAYERID,
       GIM_VALUES.GIMFORINDVGAME,
       GIM_VALUES.GAMENUMBER,
       GIM_VALUES.GIMCUMTOTAL,
       GIM_VALUES.GIMMEAN,
       case
            when GIM_VALUES.gameNumber >= 20 then GIM_VALUES.gimMean
            else
                case
                    when ALT_GIM_VALUES.gimValue is not null then (GIM_VALUES.gameNumber/20)*GIM_VALUES.gimMean + (1-GIM_VALUES.gameNumber/20)*ALT_GIM_VALUES.gimValue
                    else (GIM_VALUES.gameNumber/20)*GIM_VALUES.gimMean + (1-GIM_VALUES.gameNumber/20)*GIM_POSITION.GIM
                end
       end as 'gimValue'
from stage_hockey.gim_values_per_game GIM_VALUES
inner join season_to_next_season_mapping SEASON_MAPPING ON SEASON_MAPPING.seasonID = GIM_VALUES.seasonID
left join
     (
         select GIM_BY_PLAYER_BY_SEASON_1.seasonID,
                GIM_BY_PLAYER_BY_SEASON_1.playerID,
                case
                    when GIM_BY_PLAYER_BY_SEASON_1.gameNumber >= 20 then GIM_BY_PLAYER_BY_SEASON_1.gimMean
                    else
                        case
                            when GIM_BY_PLAYER_BY_SEASON_2.gameNumber >= 20 then GIM_BY_PLAYER_BY_SEASON_1.gimMean *
                                                                                 (GIM_BY_PLAYER_BY_SEASON_1.gameNumber / 20) +
                                                                                 GIM_BY_PLAYER_BY_SEASON_2.gimMean *
                                                                                 (1 - GIM_BY_PLAYER_BY_SEASON_1.gameNumber / 20)
                            when GIM_BY_PLAYER_BY_SEASON_2.gameNumber is null then GIM_BY_PLAYER_BY_SEASON_1.gimMean * (GIM_BY_PLAYER_BY_SEASON_1.gameNumber / 20) + GIM_POSITION.GIM * (1 - GIM_BY_PLAYER_BY_SEASON_1.gameNumber / 20)
                            else GIM_BY_PLAYER_BY_SEASON_1.gimMean * (GIM_BY_PLAYER_BY_SEASON_1.gameNumber / 20) +  (GIM_BY_PLAYER_BY_SEASON_2.gimMean *  (GIM_BY_PLAYER_BY_SEASON_2.gameNumber / 20) +  GIM_POSITION.GIM * (1 - GIM_BY_PLAYER_BY_SEASON_1.gameNumber / 20)) *  (1 - GIM_BY_PLAYER_BY_SEASON_1.gameNumber / 20)
                            end
                    end 'gimValue'
         from stage_hockey.gim_values_per_game GIM_BY_PLAYER_BY_SEASON_1
         # Joining the season and previous season mapping
         inner join season_to_next_season_mapping SEASON_MAPPING ON SEASON_MAPPING.seasonID = GIM_BY_PLAYER_BY_SEASON_1.seasonID
         left join # Getting each players previous season's GIM value
             stage_hockey.gim_values_per_game GIM_BY_PLAYER_BY_SEASON_2 ON SEASON_MAPPING.previousSeasonID = GIM_BY_PLAYER_BY_SEASON_2.seasonID and
                                                                  GIM_BY_PLAYER_BY_SEASON_1.playerID = GIM_BY_PLAYER_BY_SEASON_2.playerID
         # Joining each players position to use it to get the average GIM by position from the previous season
         inner join stage_hockey.current_positions POSITIONS on POSITIONS.playerID = GIM_BY_PLAYER_BY_SEASON_1.playerID
         # joining the average GIM by position for the previous season to use in the logic
         inner join stage_hockey.average_gim_values_by_season_position GIM_POSITION on GIM_POSITION.seasonID = SEASON_MAPPING.previousSeasonID and
                                GIM_POSITION.primaryPositionCode = POSITIONS.primaryPositionCode
         where GIM_BY_PLAYER_BY_SEASON_1.playerID = 8480800
     ) ALT_GIM_VALUES on ALT_GIM_VALUES.seasonID = SEASON_MAPPING.previousSeasonID and ALT_GIM_VALUES.playerID = GIM_VALUES.playerID
# Joining each players position to use it to get the average GIM by position from the previous season
inner join stage_hockey.current_positions POSITIONS on POSITIONS.playerID = GIM_VALUES.playerID
# joining the average GIM by position for the previous season to use in the logic
inner join stage_hockey.average_gim_values_by_season_position GIM_POSITION on GIM_POSITION.seasonID = SEASON_MAPPING.previousSeasonID and
                    GIM_POSITION.primaryPositionCode = POSITIONS.primaryPositionCode;









end;
