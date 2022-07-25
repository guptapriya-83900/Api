CREATE TABLE logindetails (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(300) NOT NULL
);

INSERT INTO logindetails (username, password) VALUES ('Sheela', '188Sheela@');
INSERT INTO logindetails (username, password) VALUES ('Gopi', 'gopi83900');
SELECT *FROM logindetails;

CREATE TABLE item (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL
);
SELECT *FROM item;

INSERT INTO item (name) VALUES ('shoes');
INSERT INTO item (name) VALUES ('bag');
INSERT INTO item (name) VALUES ('watch');
INSERT INTO item (name) VALUES ('tops');
INSERT INTO item (name) VALUES ('jeans');











