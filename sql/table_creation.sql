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




/*
Create definitions for the various keys/symbols present
*/

-- Results codes
CREATE TABLE real_estate.fact_result (
    result VARCHAR,
    definition VARCHAR
)

INSERT INTO real_estate.fact_result (result, definition) VALUES
  ('SS','Sold after auction price not disclosed')
, ('VB','Vendor bid')
, ('SN','Sold not disclosed')
, ('S','Property sold')
, ('W','Withdrawn prior to auction')
, ('SA','Sold after auction')
, ('PN','Sold prior not disclosed')
, ('SP','Property sold prior')
, ('PI','Property passed in')
, ('NB','No bid')


-- Property Types
CREATE TABLE real_estate.fact_property_type (
    prop_type VARCHAR,
    definition VARCHAR
)

INSERT INTO real_estate.fact_property_type (prop_type, definition) VALUES
  ('t','Townhouse')
, ('dev site','Development site')
, ('o res','Other residential')
, ('u','Unit')
, ('u','Duplex')
, ('h','House')
, ('h','Cottage')
, ('h','Villa')
, ('h','Semi')
, ('h','Terrace')
, ('studio','Studio')