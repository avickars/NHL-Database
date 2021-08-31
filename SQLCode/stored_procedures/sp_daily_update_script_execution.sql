CREATE procedure sp_daily_update_script_execution_view()
begin
drop table if exists production_hockey.daily_update_script_execution;
create table production_hockey.daily_update_script_execution as
select *
from daily_update_schedule
left join
(select dateOfExecution,
       max(case when script = 'get_daily_schedule' then date end ) 'get_daily_schedule',
       max(case when script = 'get_live_data' then date end ) 'get_live_data',
       max(case when script = 'get_boxscore' then date end ) 'get_boxscore',
       max(case when script = 'get_new_players' then date end ) 'get_new_players',
       max(case when script = 'create_gim_model_sequences' then date end ) 'create_gim_model_sequences',
       max(case when script = 'create_gim_values' then date end ) 'create_gim_values',
       max(case when script = 'get_new_consolidated_gims' then date end ) 'get_new_consolidated_gims',
       max(case when script = 'sp_game_prediction_team_stats_view' then date end ) 'sp_game_prediction_team_stats_view',
       max(case when script = 'get_game_outcome_predictions' then date end ) 'get_game_outcome_predictions'

from(
select cast(date as date) as 'dateOfExecution',
       script,
       max(date) as 'date'
from script_execution
where script = 'get_daily_schedule' or
       script = 'get_live_data' or
       script = 'get_boxscore' or
       script = 'get_new_players' or
      script = 'create_gim_model_sequences' or
      script = 'create_gim_values' or
      script = 'get_new_consolidated_gims' or
      script = 'sp_game_prediction_team_stats_view' or
      script = 'get_game_outcome_predictions'
group by script,cast(date as date)
    ) p group by dateOfExecution) script_executions
on daily_update_schedule.date = script_executions.dateOfExecution
where date <= curdate()
order by date desc;
end;


