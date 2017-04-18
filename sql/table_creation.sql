/*
Title:  Define All Tables
Desc:   Queries to create all required tables for the application
Author: Yassin Eltahir
Date:   2017-04-17
*/

-- Auction Results Table
-- Will add keys at a later date
CREATE TABLE real_estate.auction_results (
    suburb VARCHAR,
    address VARCHAR,
    building_type VARCHAR,
    price INT,
    result VARCHAR,
    agent VARCHAR,
    city VARCHAR,
    date DATE,
    cash_rate FLOAT
);
