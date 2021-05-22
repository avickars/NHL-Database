create database hockey;

use hockey;

insert into team_plays_in_division values (18, 26, '2021-05-21 20:19:26')

select * from team_plays_in_division

select * from divisions where divisionID=26
select * from teams where teamID=18

create table conferences (
    conferenceID int,
    conferenceName varchar(255) not null ,
    abbreviation varchar(10) not null ,
    shortName varchar(255) not null,
    primary key (conferenceID)
);

create table conference_activity(
	conferenceID int not null,
	date datetime not null,
	active bit not null
	primary key (conferenceID, date),
	foreign key (conferenceID) references conferences(conferenceID),
);

create table divisions (
    divisionID int,
    divisionName varchar(255) not null ,
    abbreviation varchar(10) not null ,
    nameShort varchar(255),
    conferenceID int null ,
    primary key (divisionID),
    foreign key (conferenceID) references conferences(conferenceID)
);

create table division_activity(
	divisionID int not null,
	date datetime not null,
	active bit not null,
	primary key(divisionID, date),
	foreign key (divisionID) references divisions(divisionID)
);

create table franchises (
    franchiseID int not null ,
    firstSeasonID int not null ,
    lastSeasonID int,
    constraint franchisesPL primary key (franchiseID)
);


create table teams (
    teamID int not null ,
	locationName varchar(255) not null,
	teamName varchar(255) not null,
    abbreviation varchar(255),
    officialSiteUrl varchar(255),
	franchiseID int,
	primary key (teamID),
	foreign key (franchiseID) references franchises (franchiseID)
);

create table team_activity(
	teamID int not null,
	date datetime not null,
	active bit not null,
	primary key(teamID, date),
	foreign key (teamID) references teams(teamID)
);

create table team_plays_in_division(
	teamID int not null,
	divisionID int,
	date datetime not null,
	primary key (teamID, date),
	foreign key (divisionID) references divisions (divisionID),
	foreign key (teamID) references teams (teamID)
);

create table team_plays_in_venue (
	venueName varchar(255),
	venueCity varchar(255),
	timeZone varchar(255),
	date datetime,
	teamID int,
	foreign key (teamID) references teams (teamID),
	primary key (date, teamID)
)

create table prospects (
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

create table prospectCategory (
	prospectCategoryID int,
    prospectCategoryName varchar(255),
	constraint prospectCategoryPK primary key (prospectCategoryID)
);



create table draftsPicks (
    draftYear smallint not null ,
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

create table seasons (
    seasonID int,
    regularSeasonStartDate date not null ,
    regularSeasonEndDate date not null ,
    seasonEndDate date not null ,
    numberOfGames int not null ,
    tiesInUse bit not null ,
    olympic_participation bit not null ,
    conferences_in_use bit not null ,
    divisions_in_use bit not null ,
    wild_card_in_use bit not null ,
    primary key (seasonID)
);

create table schedules(
	seasonID int not null,
    gameID int not null ,
    gameType char not null ,
    gameDate date not null ,
    homeTeamID int not null ,
    awayTeamID int not null ,
    primary key (gameID),
	foreign key (seasonID) references seasons(seasonID),
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
    active bit,
    date datetime,
    primary key (playerID, active, date),
    foreign key (playerID) references players (playerID)
);


create table rookies (
    playerID int,
    rookie bit,
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
    captain bit,
    date datetime,
    primary key (playerID, date),
    foreign key (playerID) references players (playerID)
);

create table alternate_captain(
    playerID int,
    alternateCaptain bit,
    date datetime,
    primary key (playerID, date),
    foreign key (playerID) references players (playerID)
);

create table plays_for (
    playerID int,
    teamID int,
    date datetime,
    primary key (playerID,teamID, date),
    foreign key (playerID) references players (playerID),
    foreign key (teamID) references teams (teamID)
);

create table positions (
	primaryPositionCode varchar(20),
    primaryPositionName varchar(255),
    primaryPositionType varchar(255),
	primary key (primaryPositionCode)
	);

create table plays_position (
    playerID int,
    primaryPositionCode varchar(20),
    date datetime,
    primary key (playerID, date),
    foreign key (playerID) references players (playerID),
	foreign key (primaryPositionCode) references positions(primaryPositionCode)
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




