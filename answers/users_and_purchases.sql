SELECT users.id, users.name, purchases.product
FROM users
FULL OUTER JOIN purchases ON users.id = purchases.id
ORDER BY users.id
