SELECT 
    r.rental_id,
    r.rental_date,
    c.customer_id,
    p.amount AS total_pago,
    ci.city AS Ciudad,
    co.country AS Pais
FROM rental r
JOIN customer c ON r.customer_id = c.customer_id
JOIN payment p ON r.rental_id = p.rental_id
JOIN address a ON c.address_id = a.address_id
JOIN city ci ON a.city_id = ci.city_id
JOIN country co ON ci.country_id = co.country_id;