CREATE procedure sp_average_gim_values_by_player_view()
begin
drop table if exists stage_hockey.average_gim_values_by_player;
create table stage_hockey.average_gim_values_by_player as
select GAMES.seasonID,
       GAMES.gameID,
       GAMES.gameType,
       GAMES.teamID,
       GAMES.playerID,
       IF(GIM.value is null, 0, GIM.value) as 'gim',
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
#                seasonID = 20202021 and
               timeOnIce is not null
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









end;
