SELECT purchases.id, users.name, purchases.product
FROM purchases
LEFT JOIN users ON purchases.id = users.id
ORDER BY purchases.id
