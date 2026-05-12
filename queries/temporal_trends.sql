# Consulta final unificada: Tendencias temporales de alquileres, ingresos y clientes
SELECT 
    DATE_FORMAT(r.rental_date, '%Y-%m-01') AS rental_date, 
    YEAR(r.rental_date) AS year, 
    MONTH(r.rental_date) AS month, 
    COUNT(r.rental_id) AS total_rentals, 
    SUM(p.amount) AS total_revenue, 
    COUNT(DISTINCT r.customer_id) AS active_customers 
FROM rental r 
LEFT JOIN payment p ON r.rental_id = p.rental_id 
GROUP BY 1, 2, 3 
ORDER BY year, month;