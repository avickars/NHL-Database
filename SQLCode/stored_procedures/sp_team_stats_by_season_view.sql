CREATE procedure sp_team_stats_by_season_view()
begin

drop table if exists stage_hockey.team_stats_by_season;
create table stage_hockey.team_stats_by_season as
select ts.seasonID,
       stnsm.seasonID nextSeasonID,
       AVG(shotsForPerGame) shotsForPerGame,
       AVG(goalsForPerGame) goalsForPerGame,
       AVG(shotsAgainstPerGame) shotsAgainstPerGame,
       AVG(goalsAgainstPerGame) goalsAgainstPerGame,
       AVG(winningPercentage) winningPercentage,
       AVG(shotDifferential) shotDifferential,
       AVG(goalDifferential) goalDifferential
from stage_hockey.game_prediction_team_stats ts
inner join
    (
        select seasonID, teamID, max(gameNumber) 'gameNumber'
        from stage_hockey.game_prediction_team_stats
        where gameType = 'R'
        group by seasonID, teamID
    ) lastGame on ts.seasonID = lastGame.seasonID and
                  ts.gameNumber = lastGame.gameNumber
inner join season_to_next_season_mapping stnsm on ts.seasonID = stnsm.previousSeasonID
group by ts.seasonID;



end;
