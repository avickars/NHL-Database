use hockey;

create table if not exists prospects (
    prospectID int primary key,
    firstName varchar(255) not null,
    lastName varchar(255) not null,
    birthDate date,
    birthCity varchar(255),
    birthStateProvince varchar(255),
    birthCountry varchar(255),
    nationality varchar(255),
    height varchar(255),
    weight int,
    shoots char,
    position char,
    nhlPlayerID int,
    prospectCategoryID int,
    prospectCategoryName varchar(255),
    amateurTeam varchar(255),
    amateurLeague varchar(255)
);

create table if not exists draftsPicks (
    draftYear year not null ,
    teamID int not null ,
    prospectID int,
    round int,
    pickInRound int,
    constraint draftsPicksPK primary key (teamID, prospectID,draftYear),
    constraint draftPickFK foreign key (prospectID) references prospects(prospectID)
);

