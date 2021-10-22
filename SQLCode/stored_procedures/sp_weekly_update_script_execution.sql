CREATE procedure sp_weekly_update_script_execution_view()
begin
drop table if exists production_hockey.weekly_update_script_execution;
create table production_hockey.weekly_update_script_execution as
select *
from weekly_update_schedule
left join
(select dateOfExecution,
       max(case when script = 'update_players' then date end ) 'update_players',
       max(case when script = 'get_new_backup_usb' then date end ) 'get_new_backup_usb',
       max(case when script = 'get_new_backup_ssd' then date end ) 'get_new_backup_ssd'

from(
select cast(date as date) as 'dateOfExecution',
       script,
       max(date) as 'date'
from script_execution
where script = 'update_players' or
       script = 'get_new_backup_usb' or
       script = 'get_new_backup_ssd'
group by script,cast(date as date)
    ) p group by dateOfExecution) script_executions
on weekly_update_schedule.date = script_executions.dateOfExecution
where date <= curdate()
order by date desc;
end;


