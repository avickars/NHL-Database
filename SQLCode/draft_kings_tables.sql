# create database draft_kings;

create table contests (
    IsStarred smallint,
    id int,
    gameType varchar(255),
    freeWithCrowns smallint,
    isBonusFinalized smallint,
    isSnakeDraft smallint,
    crownAmount int,
    IsWinnerTakeAll smallint,
    date date,
    primary key (id)
);

create table contest_details
(
    contestSummary        varchar(255),
    IsCashPrizeOnly       smallint,
    scoringStyleId        int,
    sport                 varchar(50),
    isGuaranteed          smallint,
    isPrivate             smallint,
    isResizable           smallint,
    contestStartTime      datetime,
    gameTypeId            int,
    ticketOnlyEntry       smallint,
    name                  varchar(255),
    draftGroupId          int,
    playTypeId            int,
    maximumEntries        smallint,
    maximumEntriesPerUser smallint,
    entryFee              decimal,
    crownAmount           int,
    totalPayouts          int,
    contestID             int,
    primary key (contestID),
    foreign key (contestID) references contests (id)
);

create table contest_payouts (
    minPosition int,
    maxPosition int,
    Cash decimal,
    contestID int,
    primary key (contestID, minPosition),
    foreign key (contestID) references contests (id)
);

create table contest_rules (
    gameTypeDescription varchar(255),
    salaryCapIsEnabled smallint,
    salaryCapMinValue int,
    salaryCapMaxValue int,
    gameCountIsEnabled smallint,
    gameCountMinValue int,
    gameCountMaxValue int,
    teamCountIsEnabled smallint,
    teamCountMinValue int,
    teamCountMaxValue int,
    uniquePlayers smallint,
    allowLateSwap smallint,
    gameTypeID int
);

create table contest_lineup_templates (
    id smallint,
    name varchar(20),
    description varchar(50),
    positionTip varchar(255),
    positionTipSubtext float,
    rosterSlot smallint,
    gameTypeID int,
    numInstances int,
    primary key (gameTypeID, id, numInstances)
);

create table draft_stats (
    id int,
    abbr varchar(50),
    name varchar(255),
    stat_order int,
    primary key (id)
);

create table draft_stats_players (
    id int,
    contestID int,
    value varchar(20),
    sortvalue varchar(20),
    quality varchar(50),
    playerID int,
    foreign key (contestID) references contests (id)
);

create table draft_groups_players_api (
    drafttableID int,
    firstName varchar(255),
    lastName varchar(255),
    displayName varchar(255),
    shortName varchar(255),
    playerID int,
    playerDkId int,
    position varchar(20),
    rosterSlotID int,
    salary int,
    teamAbbreviation varchar(50),
    contestID int,
    foreign key (contestID) references contests (id)
);

create table draft_groups_players_webdriver (
    position varchar(20),
    name varchar(255),
    id int,
    rosterPosition  varchar(50),
    salary int,
    gameInfo varchar(255),
    TeamAbbrev varchar(50),
    AvgPointsPerGame decimal,
    contestID int,
    foreign key (contestID) references contests (id)
);

create table contest_player_selections (
    entryID long,
    entryName varchar(255),
    lineup varchar(6535),
    contestID int,
    foreign key (contestID) references contests (id)
);

create table points_legend (
    playerType varchar(50),
    event varchar(255),
    points varchar(20),
    contestID int,
    primary key (contestID, event, playerType),
    foreign key (contestID) references contests (id)
);

create table lineup_requirements (
    lineupRequirement varchar(6535),
    contestID int,
    primary key (contestID),
    foreign key (contestID) references contests (id)
);

create table script_execution (
    script varchar(255),
    date datetime,
    primary key (script, date)
);

create table contest_game_times (
    draftGroupId int,
    homeTeamAbbreviation varchar(20),
    awayTeamAbbreviation varchar(20),
    startTime datetime,
    primary key (draftGroupId, homeTeamAbbreviation, awayTeamAbbreviation)
);