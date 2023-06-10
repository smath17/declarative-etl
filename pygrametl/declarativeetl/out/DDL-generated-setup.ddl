CREATE DATABASE test;
\connect test

CREATE TABLE Customer_Dimension
(
CustomerKEY INT PRIMARY KEY,
name VARCHAR(30),
address VARCHAR(30)
);

CREATE TABLE Part_Dimension
(
PartKEY INT PRIMARY KEY,
name VARCHAR(30),
manufacturer VARCHAR(30)
);

CREATE TABLE Date_Dimension
(
DateKEY INT PRIMARY KEY,
day INT,
month INT,
year INT
);

CREATE TABLE Lineorder_Fact_Table
(
CustomerFK INT REFERENCES Customer_Dimension,
PartFK INT REFERENCES Part_Dimension,
DateFK INT REFERENCES Date_Dimension,
quantity INT,
price DECIMAL(10, 4)
);

