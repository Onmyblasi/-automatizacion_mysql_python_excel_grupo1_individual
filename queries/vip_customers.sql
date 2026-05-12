# Consulta final: Clasificación de clientes VIP y segmentación por gasto
SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS full_name,
    ci.city,
    co.country,
    COUNT(DISTINCT r.rental_id) AS total_rentals,
    ROUND(SUM(p.amount), 2) AS total_spent,
    ROUND(AVG(p.amount), 2) AS avg_payment,
    RANK() OVER (
        ORDER BY SUM(p.amount) DESC
    ) AS vip_rank,
    CASE
        WHEN SUM(p.amount) > 150
        THEN 'VIP'
        ELSE 'Regular'
    END AS customer_segment
FROM customer c
JOIN address a ON c.address_id = a.address_id
JOIN city ci ON a.city_id = ci.city_id
JOIN country co ON ci.country_id = co.country_id
JOIN rental r ON c.customer_id = r.customer_id
JOIN payment p ON r.rental_id = p.rental_id
GROUP BY
    c.customer_id,
    full_name,
    ci.city,
    co.country
ORDER BY total_spent DESC;