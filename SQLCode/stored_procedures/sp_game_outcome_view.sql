CREATE procedure sp_games_outcomes_view()
begin
drop table if exists production_hockey.games_outcomes_view;
create table production_hockey.games_outcomes_view as
select actual.*,
       pred.prediction
from (
select GOALS.gameID,
       homeTeamID,
       IFNULL(sum(case when teamID=homeTeamID then numGoals end), 0) as 'homeTeamGoals',
       awayTeamID,
       IFNULL(sum(case when teamID=awayTeamID then numGoals end), 0) as 'awayTeamGoals'
from
     (
         select count(*) as 'numGoals',
                teamID,
                s.homeTeamID,
                s.awayTeamID,
                s.gameID
         from live_feed lf
                  inner join schedules s on lf.gameID = s.gameID and lf.teamID
         where s.seasonID >= 20142015
           and eventTypeID = 'GOAL'
           and playerType = 'Scorer'
         group by lf.gameID, lf.teamID
     ) GOALS
group by gameID ) actual
inner join stage_hockey.game_outcome_prediction pred on actual.gameID = pred.gameID
    where pred.gameID = 2014020585
end



