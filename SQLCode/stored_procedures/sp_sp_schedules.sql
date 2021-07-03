create procedure sp_schedules as
drop table production.dbo.schedules
select *
into production.dbo.schedules
from schedules
go

