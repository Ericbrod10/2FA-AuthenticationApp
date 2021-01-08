CREATE DATABASE PCN_Data;
use PCN_Data;


CREATE TABLE IF NOT EXISTS PlayerLogTable (
    id int AUTO_INCREMENT,
    LogTime DATETIME,
    player_id INT,
    Gamertag varchar(255),
    cookie varchar(255),
    CompFingerPrint varchar(2550),
    ComputerIP varchar(2550),
    MobileCookieID varchar(255),
    MobileFingerPrint varchar(2550),
    MobileIP varchar(255),
    AthCode INT,
    linkGen varchar(255),
    PRIMARY KEY (id)
);

