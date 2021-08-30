CREATE procedure sp_weekly_update_script_execution_view()
begin
drop table if exists production_hockey.weekly_update_script_execution;
create table production_hockey.weekly_update_script_execution as
select *
from weekly_update_schedule
left join
(select dateOfExecution,
       max(case when script = 'update_players' then date end ) 'update_players',
       max(case when script = 'get_new_backup' then date end ) 'get_new_backup',
       max(case when script = 'upload_backup' then date end ) 'upload_backup',
       max(case when script = 'delete_old_backup' then date end ) 'delete_old_backup'

from(
select cast(date as date) as 'dateOfExecution',
       script,
       max(date) as 'date'
from script_execution
where script = 'update_players' or
       script = 'get_new_backup' or
       script = 'upload_backup' or
       script = 'delete_old_backup'
group by script,cast(date as date)
    ) p group by dateOfExecution) script_executions
on weekly_update_schedule.date = script_executions.dateOfExecution
where date <= curdate()
order by date desc;
end;


