CREATE procedure sp_player_information_view()
begin
drop table if exists production_hockey.player_information_view;
create table production_hockey.player_information_view as
select p.playerID,
--        p.firstName,
       IF(LEFT(p.firstName, 1) = ' ', SUBSTRING(p.firstName, 2, 500), p.firstName) as 'firstName',
       IF(LEFT(p.lastName, 1) = ' ', SUBSTRING(p.lastName, 2, 500), p.lastName) as 'lastName',
--        p.lastName,
       p.birthDate,
       p.birthCity,
       p.birthCountry,
       p.height,
       p.shootsCatches,
       rosterStatus.rosterStatus,
       IF(playerActive.active = 1, playsFor.teamName, NULL) as 'Current Team',
       playerActive.active,
       headshots.headshot,
       captains.captain,
       alt_captain.alternateCaptain,
       weight.weight,
       draftPicks.teamName as 'draftTeam',
       draftPicks.pickOverall as 'pickNumber',
       draftPicks.amateurLeague,
       draftPicks.amateurTeam,
       draftPicks.pickInRound,
       draftPicks.round,
       draftPicks.draftYear,
       concat(IF(LEFT(p.firstName, 1) = ' ', SUBSTRING(p.firstName, 2, 500), p.firstName), ' ', IF(LEFT(p.lastName, 1) = ' ', SUBSTRING(p.lastName, 2, 500), p.lastName) ) as 'Name',
       draftPicks.abbreviation as 'draftTeamAbbreviation',
       p.birthStateProvince,
       positions.primaryPositionCode
from players p
left join
    (
        -- calculates if a player is on the roster
        select playerID,
               rosterStatus
        from (
                 select playerID,
                        rosterStatus,
                        row_number() over (partition by playerID order by date desc ) as 'rowNum'
                 from roster_status
             ) ha
        where ha.rowNum = 1
    ) rosterStatus on p.playerID = rosterStatus.playerID
left join
    (
        -- Calculates who a player plays for
        select playerID,
              playsFor.teamID,
              t.teamName
        from (
                select bs.playerID,
                       bs.teamID,
                       row_number() over (partition by playerID order by gameDate desc ) as 'rowNum'
                from box_scores bs
                         inner join schedules s on s.gameID = bs.gameID
            ) playsFor
                inner join teams t on playsFor.teamID = t.teamID
        where rowNum = 1
    ) playsFor on p.playerID = playsFor.playerID
left join
    (
        -- calculates of a player is active
        select playerID,
               active
        from (
               select playerID,
                      active,
                      row_number() over (partition by playerID order by date desc) as 'rowNum'
               from player_active
           ) active
        where rowNum = 1
    ) playerActive on p.playerID = playerActive.playerID
left join
    (
        -- Calculates a players current headshot picture
        select playerID,
               headshot
        from (
                 select playerID,
                        headshot,
                        row_number() over (partition by playerID order by date desc ) as 'rowNum'
                 from head_shots
             ) ha
        where ha.rowNum = 1
     ) headshots on p.playerID = headshots.playerID
left join
    (
        -- Calculates if a player is a captain
        select playerID,
               captain
        from (
                 select playerID,
                        captain,
                        row_number() over (partition by playerID order by date desc ) as 'rowNum'
                 from captain
             ) ha
        where ha.rowNum = 1
    ) captains on p.playerID = captains.playerID
left join
    (
        -- Calculates if a player is an alternate captain
        select playerID,
               alternateCaptain
        from (
                 select playerID,
                        alternateCaptain,
                        row_number() over (partition by playerID order by date desc ) as 'rowNum'
                 from alternate_captain
             ) ha
        where ha.rowNum = 1
    ) alt_captain on p.playerID = alt_captain.playerID
left join
    (
        -- calculate a players current position
        select playerID,
               primaryPositionCode
        from (
                 select playerID,
                        primaryPositionCode,
                        row_number() over (partition by playerID order by date desc ) as 'rowNum'
                 from plays_position
             ) ha
        where ha.rowNum = 1
    ) positions on p.playerID = positions.playerID
left join
    (
        -- used to join player with draft
        select nhlPlayerID,
               amateurTeam,
               amateurLeague,
               t.teamName,
               draftPicks.*,
               t.abbreviation,
               prospects.firstName,
               prospects.lastName,
               prospects.birthDate
        from prospects
        inner join
            (
                -- calculate a players draft slot
                select *
                from
                     (
                         select draftYear,
                                round,
                                pickInRound,
                                teamID,
                                prospectID,
                                pickOverall,
                                ROW_NUMBER() over (partition by prospectID, fullName order by draftYear) as 'rowNum'
                         from draft_picks
                     ) as draft
                where rowNum=1
            ) draftPicks on prospects.prospectID = draftPicks.prospectID
        inner join teams t on t.teamID = draftPicks.teamID
--         where ISNULL(nhlPlayerID, -1) <> -1
    ) draftPicks on (p.birthDate =  draftPicks.birthDate
                    and IF(LEFT(p.firstName, 1) = ' ', SUBSTRING(p.firstName, 2, 500), p.firstName) = draftPicks.firstName
                    and IF(LEFT(p.lastName, 1) = ' ', SUBSTRING(p.lastName, 2, 500), p.lastName) = draftPicks.lastName) or
                    p.playerID = draftPicks.nhlPlayerID
--         p.playerID = draftPicks.nhlPlayerID
left join
    (
        -- calculates a players current weight
        select playerID,
               weight
        from (
                 select playerID,
                        weight,
                        row_number() over (partition by playerID order by date desc ) as 'rowNum'
                 from player_weighs
             ) ha
        where ha.rowNum = 1
    ) weight on p.playerID = weight.playerID;
END

