CREATE TABLE Customer
(
CustomerKEY INT PRIMARY KEY,
name VARCHAR(30),
address VARCHAR(30)
);

CREATE TABLE Part
(
PartKEY INT PRIMARY KEY,
name VARCHAR(30),
manufacturer VARCHAR(30)
);

CREATE TABLE Date
(
DateKEY INT PRIMARY KEY,
day INT,
month INT,
year INT
);

CREATE TABLE Lineorder
(
CustomerFK INT REFERENCES Customer,
PartFK INT REFERENCES Part,
DateFK INT REFERENCES Date,
quantity INT,
price DECIMAL(10, 4)
);

