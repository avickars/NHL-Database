
drop view if exists divisions_view;

create view divisions_view as
select d.conferenceID as 'Conference ID',
       d.divisionName as 'Division Name',
       d.abbreviation as 'Division Abbreviation',
       d.divisionID
from divisions d
inner join
    (
        select divisionID,
               ROW_NUMBER() over (partition by divisionID order by date desc ) as 'rowNum'
        from division_activity
        where active=1
    ) da
on d.divisionID = da.divisionID
where rowNum = 1
