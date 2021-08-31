CREATE procedure sp_average_gim_values_by_season_position_view()
begin
drop table if exists stage_hockey.average_gim_values_by_season_position;
create table stage_hockey.average_gim_values_by_season_position as
select avgGIM.seasonID,
       AVG(avgGIM.gim) as 'GIM',
       POSITIONS.primaryPositionCode
from stage_hockey.average_gim_values_by_player avgGIM
left join
     (
         select playerID,
                primaryPositionCode
         from (
                  select playerID,
                         primaryPositionCode,
                         row_number() over (partition by playerID order by date desc ) as 'ROW_NUM'
                  from plays_position
                  where primaryPositionCode is not null
              ) POSITION
         WHERE POSITION.ROW_NUM = 1
     ) POSITIONS
on POSITIONS.playerID = avgGIM.playerID
where avgGIM.gameType = 'R'
group by avgGIM.seasonID, POSITIONS.primaryPositionCode;
end;
