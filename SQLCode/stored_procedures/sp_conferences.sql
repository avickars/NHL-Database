CREATE procedure sp_conferences_view  as
drop table if exists production.dbo.conferences_view
select c.conferenceName as 'Conference Name',
       c.abbreviation as 'Conference Abbreviation',
       c.conferenceID as 'Conference ID'
into production.dbo.conferences_view
from conferences c
inner join
    (
        select conferenceID,
               ROW_NUMBER() over (partition by conferenceID order by date desc ) as 'rowNum'
        from conference_activity
        where active=1
    ) ca
on c.conferenceID = ca.conferenceID
where rowNum = 1
go

