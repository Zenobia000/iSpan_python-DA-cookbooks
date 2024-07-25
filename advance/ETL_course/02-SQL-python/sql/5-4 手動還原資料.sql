/* 將老師編號為 T001 的姓名，改成 曾○○ */
UPDATE `teachers`
SET `tName` = '曾○○'
WHERE `tId` = 'T001';

/* 新增一筆資料，學生編號為 088、課程編號為 C004，成績為 94 */
INSERT INTO `scores` 
(`sId`, `cId`, `score`) 
VALUES
('088', 'C004', 94);
