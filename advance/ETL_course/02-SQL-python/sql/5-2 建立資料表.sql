/* students（學生資料表） */
CREATE TABLE `my_db`.`students` (
    `sId` VARCHAR(3) NOT NULL COMMENT '學生編號',
    `sName` VARCHAR(20) NOT NULL COMMENT '學生姓名',
    `sGender` VARCHAR(1) NOT NULL COMMENT '學生性別',
    `sNickname` VARCHAR(50) NOT NULL COMMENT '學生暱稱',
    PRIMARY KEY (`sId`)
) COMMENT = '學生資料表';


/* scores（成績資料表） */
CREATE TABLE `my_db`.`scores` ( 
    `sId` VARCHAR(3) NOT NULL COMMENT '學生編號', 
    `cId` VARCHAR(4) NOT NULL COMMENT '課程編號', 
    `score` TINYINT(3) NOT NULL COMMENT '成績',
    PRIMARY KEY (`sId`,`cId`)
) COMMENT = '成績資料表';


/* teachers（老師資料表） */
CREATE TABLE `my_db`.`teachers` ( 
    `tId` VARCHAR(4) NOT NULL COMMENT '老師編號' , 
    `tName` VARCHAR(10) NOT NULL COMMENT '老師姓名',
    PRIMARY KEY (`tId`)
) COMMENT = '老師資料表';


/* courses（課程資料表） */
CREATE TABLE `my_db`.`courses` ( 
    `cId` VARCHAR(4) NOT NULL COMMENT '課程編號', 
    `cName` VARCHAR(10) NOT NULL COMMENT '課程名稱', 
    `credit` TINYINT(1) NOT NULL COMMENT '學分', 
    `isCompulsory` TINYINT(1) NOT NULL COMMENT '是否必修', 
    `tId` VARCHAR(4) NOT NULL COMMENT '老師編號',
    PRIMARY KEY (`cId`, `tId`)
) COMMENT = '課程資料表';

