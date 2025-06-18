SELECT employee, department, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rank_in_dept
FROM employees
