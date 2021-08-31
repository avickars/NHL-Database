create database hockey;
use hockey;


create table conferences (
    conferenceID int,
    conferenceName varchar(255) not null ,
    abbreviation varchar(10) not null ,
    shortName varchar(255) not null,
    primary key (conferenceID)
);

create table conference_activity (
    conferenceID int not null,
    date datetime not null,
    active bool not null ,
    primary key (conferenceID, date),
    foreign key (conferenceID) references conferences(conferenceID)
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
	active bool not null,
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
	active bool not null,
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
);


create table seasons (
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
	seasonID int not null,
    gameID int not null ,
    gameType varchar(20) not null ,  -- this has to be a varchar(20) because the are a couple types that are multiple letters
    gameDate date not null ,
    homeTeamID int not null ,
    awayTeamID int not null ,
    gameDateTime datetime not null ,
    primary key (gameID),
	foreign key (seasonID) references seasons(seasonID),
    foreign key (homeTeamID) references teams (teamID),
    foreign key (awayTeamID) references teams (teamID)
);


create table script_execution (
    script varchar(255),
    date datetime,
    primary key (script, date)
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
    shootsCatches char(1),
    primary key (playerID)
);


create table roster_status (
    playerID int,
    rosterStatus char(1),
    date datetime,
    primary key (playerID, date),
    foreign key (playerID) references players (playerID)
);

create table player_weighs (
    playerID int,
    weight int,
    date datetime,
    primary key (playerID, date),
    foreign key (playerID) references players (playerID)
);


create table player_active (
    playerID int,
    active bool,
    date datetime,
    primary key (playerID, active, date),
    foreign key (playerID) references players (playerID)
);

create table plays_for (
    playerID int,
    teamID int,
    date datetime,
#     primary key (playerID, teamID, date),
    foreign key (playerID) references players (playerID) on delete cascade ,
    foreign key (teamID) references teams (teamID) on delete cascade
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

create table rookies (
    playerID int,
    rookie bool,
    date datetime,
    primary key (playerID, date),
    foreign key (playerID) references players (playerID)
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
    shoots char(1),
    position char,
    nhlPlayerID int,
    prospectCategoryID int,
    prospectCategoryName varchar(255),
    amateurTeam varchar(255),
    amateurLeague varchar(255),
    constraint prospectPK primary key (prospectID)
);



create table draft_picks (
    draftYear smallint not null ,
    round int not null ,
    pickOverall int not null ,
    pickInRound int not null ,
    teamID int not null ,
    prospectID int null ,
    fullName varchar(255) not null ,
    constraint draftsPicksPK primary key (draftYear,pickOverall),
    constraint draftPickFKTeam foreign key (teamID) references teams(teamID)
);


create table live_feed(
    eventID int,
    eventSubID int,
    gameID int,
    event varchar(255),
    eventCode varchar(255),
    eventTypeID varchar(255),
    eventDescription varchar(255),
    secondaryType varchar(255),
    periodNum varchar(255),
    periodTime time,
    playerID int,
    playerType varchar(255),
    xCoordinate decimal,
    yCoordinate decimal,
    teamID int,
    penaltySeverity varchar(255),
    penaltyMinutes int,
    strength varchar(255),
    gameWinningGoal bool,
    emptyNetGoal bool,
    primary key (gameID, eventID, eventSubID),
    foreign key (gameID) references schedules(gameID),
    foreign key (teamID) references teams (teamID)
);

create table box_scores (
    gameID int,
    teamID int,
    playerID int,
    jerseyNumber int,
    timeOnIce varchar(255),
    plusMinus int,
    evenTimeOnIce varchar(255),
    powerPlayTimeOnIce varchar(255),
    shortHandedTimeOnIce varchar(255),
    unknown bool,
    scratched bool,
    primary key (gameID, teamID, playerID),
    foreign key (gameID) references schedules (gameID),
    foreign key (teamID) references teams (teamID)
);

create table head_shots (
    playerID int,
    headshot varchar(255),
    date datetime,
    primary key (playerID,date)
);

create table trophies (
    trophyID int,
    categoryID int,
    description varchar(255),
    imageURL varchar(255),
    name varchar(255),
    shortName varchar(255),
    primary key (trophyID)
);

create table trophy_winners (
    awardedPosthumously bool,
    coachID int,
    isRookie bool,
    playerID int,
    seasonID int,
    status varchar(255),
    teamID int,
    trophyID int,
    voteCount int,
    imageURl varchar(255),
    fullName varchar(255),
    primary key (coachID, playerID, seasonID, trophyID, fullName),
    foreign key (trophyID) references trophies (trophyID)
);

create table daily_update_schedule (
    date date,
    primary key (date)
);

create table weekly_update_schedule (
    date date,
    primary key (date)
);

create table yearly_update_schedule (
    date date,
    primary key (date)
);

create table stage_hockey.gim_sequences (
    gameID int,
    goalDiff int,
    manpowerDiff int,
    periodNum int,
    sequenceNum int,
    eventNum int,
    secondsElapsed int,
    xCoord int,
    yCoord int,
    playerID int,
    assist bit,
    blocked_shot bit,
    faceoff bit,
    giveaway bit,
    goal bit,
    hit bit,
    missed_shot bit,
    penalty bit,
    shot bit,
    takeaway bit,
    away bit,
    home bit,
    primary key (gameID,
                sequenceNum,
                eventNum)
);

create table stage_hockey.gim_values (
    gameID int,
    sequenceNum int,
    eventNum int,
    playerID int,
    awayTeam smallint,
    homeTeam smallint,
    homeProbability float,
    awayProbability float,
    neitherProbability float,
    primary key (gameID, sequenceNum, eventNum),
    foreign key (gameID, sequenceNum, eventNum) references stage_hockey.gim_sequences (gameID,sequenceNum,eventNum)
);

create table season_to_next_season_mapping(
    seasonID int,
    previousSeasonID int,
    foreign key (seasonID) references seasons (seasonID),
    foreign key (previousSeasonID) references seasons (seasonID),
    primary key (seasonID, previousSeasonID)
);

insert into season_to_next_season_mapping
values (20112012, 20102011),
       (20122013, 20112012),
       (20132014, 20122013),
       (20142015, 20132014),
       (20152016, 20142015),
       (20162017, 20152016),
       (20172018, 20162017),
       (20182019, 20172018),
       (20192020, 20182019),
       (20202021, 20192020)

create table stage_hockey.gim_values_consolidated (
    seasonID int,
    gameID int,
    gameType char(1),
    teamID int,
    playerID int,
    gimForIndvGame float,
    gameNumber int,
    gimCumTotal float,
    gimMean float,
    gimMeanAdjusted float,
    primary key (seasonID, gameID, playerID)
);

create table stage_hockey.gim_by_player_by_season (
    seasonID int,
    playerID int,
    gimValueAdjusted float,
    primary key (seasonID, playerID)
);

create table stage_hockey.gim_position_averages_per_season (
    seasonID int,
    primaryPositionCode char(1),
    gimMean float,
    primary key (seasonID, primaryPositionCode)
);

create table stage_hockey.game_outcome_prediction (
    gameID int,
    homeTeamID int,
    awayTeamID int,
    prediction smallint,
    primary key (gameID)
);

create table team_logos (
    franchiseID int,
    teamID int,
    startSeason int,
    endSeason int,
    logoID int,
    logoURL varchar(250),
    background varchar(20),
    primary key (franchiseID, teamID, logoID),
    foreign key (teamID) references teams (teamID),
    foreign key (franchiseID) references franchises (franchiseID)
);


