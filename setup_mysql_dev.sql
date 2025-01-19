-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS my_appointment_db;
CREATE USER IF NOT EXISTS 'my_dev'@'localhost' IDENTIFIED BY 'my_dev_pwd';
GRANT ALL PRIVILEGES ON `my_appointment_db`.* TO 'my_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'my_dev'@'localhost';
FLUSH PRIVILEGES;
