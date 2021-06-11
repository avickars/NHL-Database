drop view if exists trophy_winners_view

create view trophy_winners_view as
select seasonID,
       teamID,
       playerID,
       t.name,
       status
from trophy_winners
inner join trophies t on t.trophyID = trophy_winners.trophyID
where playerID <> -1

select * from trophies


select *
from draft_picks inner join prospects p on draft_picks.prospectID = p.prospectID inner join players p2 on p2.playerID = p.nhlPlayerID where p2.lastName='Sydney'