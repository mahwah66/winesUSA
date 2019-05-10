-- Create the database and use it
CREATE DATABASE wine_db;
USE wine_db;

-- Put new tables into the database
CREATE TABLE sample_table (
  column1 VARCHAR(50) NOT NULL,
  column2 INT,
  column3 BOOLEAN DEFAULT false
);

INSERT INTO sample_table (column1, column2, column3)
VALUES ("Data 1", 1, true);
-- If giving all columns can skip
INSERT INTO sample_table
VALUES 
  ("Data 2", 2, true),
  ("Data 4", 4, true)
  ;
INSERT INTO sample_table (column1)
VALUES ("Data 3");
-- updating when not is safe mode
UPDATE sample_table
SET column2 = 3
WHERE column1 = "Data 3";
-- Show the table
SELECT * FROM sample_table;

CREATE TABLE sample_table2 (
  id INT AUTO_INCREMENT NOT NULL,
  column1 VARCHAR(50) NOT NULL,
  column2 INT,
  column3 BOOLEAN DEFAULT false,
  column4 DECIMAL (20,2),
  PRIMARY KEY (id)
);
INSERT INTO sample_table2 (column1, column2, column3)
VALUES ("Data 1", 1, true);

SELECT * FROM sample_table2;

ALTER TABLE sample_table2
  ADD column5 boolean default true;

ALTER TABLE globalfirepower
  ADD id INT AUTO_INCREMENT NOT NULL PRIMARY KEY FIRST;

-- JOINS
-- SELECT title, firstName, lastName
-- FROM books
-- INNER JOIN authors ON books.authorId = authors.id;
-- Can also use left and right, outer joins

-- SELECT b.title, a.firstName, a.lastName
-- FROM books as b
-- RIGHT JOIN authors as a ON b.authorId = a.id;
-- IMPORT CSV
-- Create database; rightclick on tables and do a table data import
-- Right click on table and alter table and select primary key - then hit apply

-- SELECTING
-- SELECT * FROM TableName
-- SELECT column1 FROM TableName
-- SELECT * FROM TableName WHERE column1 = "Acanthis" AND/OR column2 = "Netherlands";
-- SELECT * FROM TableName WHERE NOT column1 = "Anthus";
-- SELECT MIN(column1) FROM TableName WHERE column2 = "CC";
-- SELECT COUNT(*) FROM TableName;

-- SET SQL_SAFE_UPDATES = 0;
-- DELETE FROM table_name WHERE condition;

-- UPDATE tableName
-- SET column1=value1, column2=value2,...
-- WHERE filterColumn=filterValue;
 
-- SELECT AVG(TotalMilitaryPersonnel) INTO @var1 FROM globalfirepower;
-- Use the ` (backtic) not the ' around values that look bad

 -- DESCRIBE to see the details of a table
 
-- GROUPINGS to do counts average etc. Use HAVING after the groupby
USE sakila;
SELECT rating, COUNT(film_id) as 'Total_count'
FROM film
-- WHERE rating !='G'
GROUP BY rating
HAVING rating!='G' 
ORDER BY Total_count DESC; -- Or ASC

-- SUBQUERIES
SELECT *
FROM inventory
WHERE film_id
IN (
	SELECT film_id
	FROM film
	WHERE title = 'Early Home'
);

Select first_name, last_name
From customer
WHERE address_id
IN(	
	Select address_id
	from address
	WHERE city_id
	IN(
		SElECT city_id
		FROM city
		-- WHERE city IN('Qalyub','Qinhuangdao','Qomsheh','Quilmes')
		WHERE city LIKE 'Q%'
));

-- SAVING QUERIES INTO A TABLE OR VIEWS
-- CREATE VIEW view_name as ...list the query(ies)

SELECT title, (SELECT COUNT(*) FROM inventory
    WHERE film.film_id = inventory.film_id) AS "Number of copies"
From film;

-- Foreign keys
-- FOREIGN KEY (column_name) REFERENCES other_table(original_column)
CREATE TABLE customer_email (
    id INTEGER(11) AUTO_INCREMENT NOT NULL,
    email VARCHAR(30) NOT NULL,
    customer_id INTEGER(11) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (customer_id) REFERENCES customer(id)
);

-- INSERT A QUERY INTO A TABLE: FIRST CREATE THE TABLE AND THEN:
INSERT INTO customer_phone (phone, customer_id)
SELECT phone, id
FROM customer;
SELECT * FROM customer_phone;

-- UNIONS where you are concatenating two similar tables
SELECT actor_id AS id, first_name
FROM actor
WHERE actor_id between 1 and 5
UNION -- UNION ALL to include duplicates
SELECT customer_id AS id, first_name
FROM customer
WHERE customer_id between 6 and 10;

SELECT UPPER(CONCAT (first_name, " ", last_name))
FROM actor;