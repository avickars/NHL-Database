use hockey;

create table if not exists prospects (
    prospectID int ,
    firstName varchar(255) not null,
    lastName varchar(255) not null,
    birthDate date,
    birthCity varchar(255),
    birthStateProvince varchar(255),
    birthCountry varchar(255),
    height varchar(255),
    weight int,
    shoots char,
    position char,
    nhlPlayerID int,
    prospectCategoryID int,
    prospectCategoryName varchar(255),
    amateurTeam varchar(255),
    amateurLeague varchar(255),
    constraint prospectPK primary key (prospectID)
);

create table if not exists conferences (
    conferenceID int,
    conferenceName varchar(255) not null ,
    abbreviation varchar(10) not null ,
    shortName varchar(255) not null ,
    active bool not null ,
    primary key (conferenceID)
);

create table if not exists divisions (
    divisionID int,
    divisionName varchar(255) not null ,
    abbreviation varchar(10) not null ,
    nameShort varchar(255),
    conferenceID int null ,
    active bool not null ,
    primary key (divisionID),
    foreign key (conferenceID) references conferences (conferenceID)
);

create table if not exists franchises (
    franchiseID int not null ,
    firstSeasonID int not null ,
    lastSeasonID int,
    mostRecentTeamID int not null ,
    teamName varchar(255)  not null ,
    locationName varchar(255)  not null ,
    constraint franchisesPL primary key (franchiseID)
);

create table if not exists teams (
    teamID int not null ,
    venueName varchar(255),
    venueCity varchar(255),
    timeZone varchar(255),
    abbreviation varchar(255),
    divisionID int,
    officialSiteUrl varchar(255),
    franchiseID int not null ,
    active bool not null ,
    constraint teamPK primary key (teamID),
    constraint teamsFKFranchise foreign key (franchiseID) references franchises(franchiseID),
    constraint teamsFKDivision foreign key (divisionID) references divisions(divisionID)
);

create table if not exists draftsPicks (
    draftYear year not null ,
    round int not null ,
    pickOverall int not null ,
    pickInRound int not null ,
    teamID int not null ,
    prospectID int null ,
    fullName varchar(255) not null ,
    constraint draftsPicksPK primary key (draftYear,pickOverall),
    constraint draftPickFKTeam foreign key (teamID) references teams(teamID),
    constraint draftPickFKProspects foreign key (prospectID) references prospects (prospectID)
);

create table if not exists seasons (
    seasonID int,
    regularSeasonStartDate date not null ,
    regularSeasonEndDate date not null ,
    seasonEndDate date not null ,
    numberOfGames int not null ,
    tiesInUse bool not null ,
    olympic_participation bool not null ,
    conferences_in_use bool not null ,
    divisions_in_use bool not null ,
    wild_card_in_use bool not null ,
    primary key (seasonID)
);

create table schedules(
    gameID int not null ,
    gameType char not null ,
    gameDate date not null ,
    homeTeamID int not null ,
    awayTeamID int not null ,
    primary key (gameID),
    foreign key (homeTeamID) references teams (teamID),
    foreign key (awayTeamID) references teams (teamID)
);

create table players (
    playerID int,
    firstName varchar(255),
    lastName varchar(255),
    birthDate date,
    birthCity varchar(255),
    birthStateProvince varchar(255),
    birthCountry varchar(255),
    height varchar(255),
    weight int,
    shootsCatches char(1),
    rosterStatus char(1),
    primary key (playerID)
);

create table active (
    playerID int,
    active bool,
    date datetime,
    primary key (playerID, active, date),
    foreign key (playerID) references players (playerID)
);


create table rookies (
    playerID int,
    rookie bool,
    date datetime,
    primary key (playerID, date),
    foreign key (playerID) references players (playerID)
);

create table wears_number (
    playerID int,
    primaryNumber int,
    date datetime,
    primary key (playerID, date),
    foreign key (playerID) references players (playerID)
);

create table captain(
    playerID int,
    captain bool,
    date datetime,
    primary key (playerID, date),
    foreign key (playerID) references players (playerID)
);

create table alternate_captain(
    playerID int,
    alternateCaptain bool,
    date datetime,
    primary key (playerID, date),
    foreign key (playerID) references players (playerID)
);

create table plays_for (
    playerID int,
    teamID int,
    date datetime,
    primary key (playerID,date),
    foreign key (playerID) references players (playerID),
    foreign key (teamID) references teams (teamID)
);

create table position (
    playerID int,
    primaryPositionCode varchar(20),
    primaryPositionName varchar(255),
    primaryPositionType varchar(255),
    date datetime,
    primary key (playerID, date),
    foreign key (playerID) references players (playerID)
);

create table live_feed (
    eventID int,
    gameID int,
    event varchar(255),
    eventCode varchar(255),
    eventTypeID varchar(255),
    eventDescription varchar(255),
    secondaryType varchar(255),
    periodNum varchar(255),
    periodTime time,
    playerOneID int,
    playerTwoID int,
    xCoordinate decimal,
    yCoordinate decimal,
    primary key (gameID, eventID),
    foreign key (gameID) references schedules(gameID),
    foreign key (playerOneID) references players (playerID),
    foreign key (playerTwoID) references players (playerID)
);



