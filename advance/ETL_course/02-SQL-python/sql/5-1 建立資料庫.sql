/* 如果資料庫存在就刪除 */
DROP DATABASE IF EXISTS `my_db`;

/* 若資料庫不存在則新增，預設字元集為 utf8mb4，定序為 utf8mb4_unicode_ci */
CREATE DATABASE IF NOT EXISTS `my_db` 
DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

/* 指定資料庫 */
USE `my_db`;