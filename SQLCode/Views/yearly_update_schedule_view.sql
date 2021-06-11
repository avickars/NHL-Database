drop view if exists yearly_update_script_execution

create view yearly_update_script_execution as
select YUS.date,
       cast(get_conferences as time) as 'get_conferences',
       cast(get_divisions as time) as 'get_divisions',
       cast(get_franchises as time) as 'get_franchises',
       cast(get_teams as time) as 'get_teams',
       cast(get_seasons as time) as 'get_seasons',
       cast(get_drafts as time) as 'get_drafts',
       cast(update_prospects as time) as 'update_prospects',
       cast(get_trophies as time) as 'get_trophies',
       cast(get_trophy_winners as time) as 'get_trophy_winners'
from yearly_update_schedule YUS
left join
    (
        select dateOfExecution,
               [get_conferences],
               [get_divisions],
               [get_franchises],
               [get_teams],
               [get_seasons],
               [get_drafts],
               [update_prospects],
               [get_trophies],
               [get_trophy_winners]
        from
             (
                 select script,
                        CAST(date AS date) as 'dateOfExecution',
                        date
                 from script_execution
                 where script = 'get_conferences' or
                       script = 'get_divisions' or
                       script = 'get_franchises' or
                       script = 'get_teams' or
                       script = 'get_seasons' or
                       script = 'get_drafts' or
                       script = 'update_prospects' or
                       script = 'get_trophies' or
                       script = 'get_trophy_winners'
             ) as sourceTable
        pivot (
                 max(date) for script
                 in (
                     [get_conferences],
                     [get_divisions],
                     [get_franchises],
                     [get_teams],
                     [get_seasons],
                     [get_drafts],
                     [update_prospects],
                     [get_trophies],
                     [get_trophy_winners]
                     )
                 ) as pivotTable
    ) SE on YUS.date = SE.dateOfExecution
where YUS.date <= getdate()
