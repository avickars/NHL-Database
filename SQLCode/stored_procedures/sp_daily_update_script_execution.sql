CREATE procedure daily_update_script_execution as
drop table production.dbo.daily_update_script_execution
select DUS.date,
       cast(SE.get_live_data as time) as 'get_live_data',
       cast(SE.get_daily_schedule as time) as 'get_daily_schedule',
       cast(SE.get_boxscore as time) as 'get_boxscore',
       cast(SE.get_new_players as time) as 'get_new_players'
into production.dbo.daily_update_script_execution
from daily_update_schedule DUS
left join
    (
        select dateOfExecution, [get_daily_schedule], [get_live_data], [get_boxscore], [get_new_players]
    from
         (
             select script,
                    cast(date as date) as 'dateOfExecution',
                    date
             from script_execution
             where script = 'get_daily_schedule' or
                   script = 'get_live_data' or
                   script = 'get_boxscore' or
                   script = 'get_new_players'
         ) as sourceTable
    pivot (
             max(date) for script in ([get_daily_schedule], [get_live_data], [get_boxscore], [get_new_players])
          ) as pivotTable
    ) SE on DUS.date = SE.dateOfExecution
where DUS.date <= getdate()
go

