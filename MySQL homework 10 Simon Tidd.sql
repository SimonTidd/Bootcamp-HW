USE sakila;
#1a
SELECT first_name, last_name
FROM actor;

#1b
SELECT first_name, last_name, CONCAT(UPPER(first_name)," ",UPPER(last_name))
	AS name
FROM actor;

#2a
SELECT *
FROM actor
WHERE first_name='Joe';

#2b
SELECT * 
FROM actor
WHERE last_name LIKE "%GEN%";

#2c
SELECT * 
FROM actor
WHERE last_name LIKE "%LI%"
ORDER BY last_name, first_name;


#2d
SELECT country_id, country
FROM country
WHERE country IN('Afghanistan','Bangladesh','China');

#3a
ALTER TABLE actor
ADD (description blob);

#3b
ALTER TABLE actor
DROP COLUMN description;

#4a
SELECT last_name,COUNT(*)
FROM actor
GROUP BY last_name;

#4b
SELECT last_name,COUNT(*)
FROM actor
GROUP BY last_name
HAVING COUNT(*)>1;

#4c
UPDATE actor SET first_name = REPLACE(first_name, 'GROUCHO', 'HARPO') WHERE last_name ='WILLIAMS';

#4d
UPDATE actor SET first_name = REPLACE(first_name, 'HARPO', 'GROUCHO') WHERE actor_ID>0 and first_name ='HARPO';

#5a
SHOW CREATE TABLE address;


#6a
SELECT first_name, last_name, address
FROM staff INNER JOIN address
ON staff.address_id=address.address_id;

#6b
SELECT first_name, last_name, SUM(amount) AS Total
FROM staff INNER JOIN payment
ON staff.staff_id=payment.staff_id
WHERE payment_date LIKE "%2005-08%"
GROUP BY payment.staff_id;

#6c
SELECT title, COUNT(DISTINCT(actor_id)) AS actors
FROM film INNER JOIN film_actor
ON film.film_id=film_actor.film_id
GROUP BY film.title;


#6d
SELECT title, COUNT(inventory.film_id) AS total
FROM film INNER JOIN inventory
ON film.film_id=inventory.film_id
WHERE title='Hunchback Impossible';

#6e
SELECT first_name, last_name, SUM(amount) AS Total
FROM customer INNER JOIN payment
ON customer.customer_id=payment.customer_id
GROUP BY customer.customer_id
ORDER BY customer.last_name;

#7a
#couldn't get this one working
#SELECT title
#FROM film
#WHERE language_id = 1 (SELECT title FROM film WHERE (title LIKE 'K%' IS TRUE or title LIKE 'Q%' IS TRUE));

#7b
SELECT first_name, last_name
FROM actor
WHERE actor_id IN (SELECT actor_id FROM film WHERE title = 'Alone Trip');

#7c
SELECT first_name, last_name, email
FROM customer INNER JOIN customer_list
ON customer.customer_id=customer_list.ID
WHERE customer_list.country='Canada';

#7d
SELECT title
FROM film
WHERE film_id IN (SELECT film_id FROM film_category WHERE category_id IN (SELECT category_id FROM category WHERE name='family'));

# couldn't crack 7e-h

# for 8a using 7c for the view below

CREATE VIEW country_email_list AS
SELECT first_name, last_name, email, country
FROM customer INNER JOIN customer_list
ON customer.customer_id=customer_list.ID;

#to display the view selecting a focal country
SELECT * FROM country_email_list
WHERE country='Canada'; 

#use the following to delete view
DROP VIEW 'sakila'.'country_email_list'