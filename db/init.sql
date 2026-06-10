CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content VARCHAR(255) NOT NULL
);

INSERT INTO messages (content) VALUES ('Success! This message was retrieved from the MySQL Database.');
