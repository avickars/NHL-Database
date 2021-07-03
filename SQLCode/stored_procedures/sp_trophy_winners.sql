create procedure trophy_winners_view as
drop table production.dbo.trophy_winners_view
select seasonID,
       teamID,
       playerID,
       t.name,
       status
into production.dbo.trophy_winners_view
from trophy_winners
inner join trophies t on t.trophyID = trophy_winners.trophyID
where playerID <> -1
go

