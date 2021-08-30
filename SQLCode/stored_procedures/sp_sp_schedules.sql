create procedure sp_schedules_view()
begin
drop table if exists production_hockey.schedules;
create table production_hockey.schedules
select *
from schedules
where gameDate < current_date();
end

