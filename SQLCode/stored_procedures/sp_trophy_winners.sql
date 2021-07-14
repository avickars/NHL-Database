create procedure sp_trophy_winners_view()
begin
drop table if exists production_hockey.trophy_winners_view;
create table production_hockey.trophy_winners_view as
select seasonID,
       teamID,
       playerID,
       t.name,
       status
from trophy_winners
inner join trophies t on t.trophyID = trophy_winners.trophyID
where playerID <> -1;
end

