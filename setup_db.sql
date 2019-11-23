CREATE DATABASE IF NOT EXISTS Anonymisation;
use Anonymisation;
CREATE USER IF NOT EXISTS 'anonymisation'@'localhost' IDENTIFIED BY 'azerty';
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER ON Anonymisation.* TO 'anonymisation'@'localhost';

CREATE TABLE IF NOT EXISTS ground_truth (
    id_user VARCHAR(5),
    date DATE,
    hours TIME,
    id_item VARCHAR(5),
    price FLOAT,
    qty INT
);
