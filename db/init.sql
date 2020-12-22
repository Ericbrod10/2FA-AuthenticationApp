CREATE DATABASE CheckInData;
use CheckInData;


CREATE TABLE IF NOT EXISTS LogTable (
    id int AUTO_INCREMENT,
    FirstName varchar(255),
    LastName varchar(255),
    PhoneNumber varchar(255),
    ReasonForVisit varchar(255),
    LoginCookieID varchar(255),
    CheckInTime DATETIME,
    CheckOutTime DATETIME,
    PRIMARY KEY (id)
);

INSERT INTO LogTable VALUES
    (1 ,'FnameTest', 'LnameTest', '555-555-5555','Shopping','Example_Cookie_gfhjdsghjfdbhjdsfdfdfssdf', '2020-12-10 11:18:53', '2020-12-14 12:18:53');
