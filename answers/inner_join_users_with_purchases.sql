SELECT users.id, users.name, purchases.product
FROM users
INNER JOIN purchases ON users.id = purchases.id
ORDER BY users.id
