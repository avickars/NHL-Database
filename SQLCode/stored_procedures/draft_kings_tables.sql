create database draft_kings;

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