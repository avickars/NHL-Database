drop view if exists conferences_view;

create view conferences_view as
select c.conferenceName as 'Conference Name',
       c.abbreviation as 'Conference Abbreviation',
       c.conferenceID as 'Conference ID'
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
