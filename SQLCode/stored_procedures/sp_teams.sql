create procedure sp_teams_view()
begin
drop table if exists production_hockey.teams_view;
create table production_hockey.teams_view as
select t.teamID as 'Team ID',
       t.locationName as 'Team Location Name',
       t.teamName as 'Team Name',
       t.abbreviation as 'Team Abbreviation',
       tv.venueCity as 'Venue City',
       tv.venueName as 'Venue Name',
       tv.timeZone as 'Venue Time Zone',
       f.firstSeasonID as 'First Season',
       da.divisionID as 'Division ID'
from teams t
inner join
    (select teamID
    from (select *,
                 row_number() over (partition by teamID order by date desc ) as rowNum
            from team_activity) r
    where r.rowNum = 1) ta
on t.teamID = ta.teamID
inner join
    (select teamID, divisionID
    from (select *,
             row_number() over (partition by teamID order by date desc ) as rowNum
        from team_plays_in_division) r where r.rowNum = 1) da
on t.teamID = da.teamID
inner join
    (select venueCity, venueName, timeZone, teamID
    from (select *,
                 row_number() over (partition by teamID order by date desc ) as rowNum
    from team_plays_in_venue) r where r.rowNum = 1) as tv
on t.teamID = tv.teamID
inner join franchises f on f.franchiseID = t.franchiseID;
end

