drop view if exists conferences_view;

create view conferences_view as
select c.conferenceName as 'Conference Name', c.abbreviation as 'Conference Abbreviation', c.conferenceID as 'Conference ID'
from conferences c
inner join conference_activity ca on c.conferenceID = ca.conferenceID
where ca.active = 1;

drop view if exists divisions_view;

create view divisions_view as
select d.conferenceID as 'Conference ID', d.divisionName as 'Division Name', d.abbreviation as 'Division Abbreviation', d.divisionID
from divisions d
inner join division_activity da on d.divisionID = da.divisionID
where da.active = 1;

drop view if exists teams_view;

create view teams_view as
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
            from team_activity where active = 1 or teamID=55) r
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


select lf.playerID, count(*)
from live_feed_temp lf
inner join schedules s
    on s.gameID = lf.gameID
where lf.eventTypeID = 'GOAL' and
      lf.playerType = 'Scorer' and
      (s.gameType='R' or s.gameType='P')

-- GOALS
select lf.playerID, s.gameType, s.seasonID,count(*) as 'goals'
from live_feed_temp lf
inner join schedules s
    on s.gameID = lf.gameID
where lf.eventTypeID = 'GOAL' and
      lf.playerType = 'Scorer' and
      (s.gameType='R' or s.gameType='P')
group by lf.playerID, s.gameType, s.seasonID

-- ASSISTS
select lf.playerID, s.gameType, s.seasonID,count(*) as 'assists'
from live_feed_temp lf
inner join schedules s
    on s.gameID = lf.gameID
where lf.eventTypeID = 'GOAL' and
      lf.playerType = 'Assist' and
      (s.gameType='R' or s.gameType='P')
group by lf.playerID, s.gameType, s.seasonID




select lf.*, t.teamName
from live_feed_temp lf
inner join teams t
    on lf.teamID = t.teamID
where lf.eventTypeID='SHOT'



select distinct lf.gameID,lf.playerID, lf.teamID,t.teamName
from live_feed_temp lf
inner join teams t
    on lf.teamID = t.teamID
where (eventTypeID = 'FACEOFF' and playerType = 'Winner') or
      (eventTypeID = 'HIT' and playerType = 'HITTER') or
      (eventTypeID = 'PENALTY' and playerType = 'PenaltyOn') or
      (eventTypeID = 'GOAL' and (playerType = ' Scorer' or playerType = 'Assist')) or
      (eventTypeID = 'SHOT' and playerType = 'Shooter') or
      (eventTypeID = 'GIVEAWAY' and playerType = 'PlayerID') or
      (eventTypeID = 'MISSED_SHOT' and playerType = 'MIssed Shot') or
      (eventTypeID = 'Takeaway' and playerType='PlayerID')


















