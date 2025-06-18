import io
import duckdb
import pandas as pd

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ------------------------------------------------------------------------------
# EXERCISES LIST
# ------------------------------------------------------------------------------

exercises = [
    {
        "theme": "cross_joins",
        "exercise_name": "beverages_and_food",
        "tables": ["beverages", "food_items"],
        "description": "Affiche toutes les combinaisons possibles entre les boissons et les aliments disponibles."
    },
    {
        "theme": "cross_joins",
        "exercise_name": "sizes_and_trademarks",
        "tables": ["sizes", "trademarks"],
        "description": "Génère toutes les combinaisons entre tailles et marques pour des vêtements fictifs."
    },
    {
        "theme": "group_by",
        "exercise_name": "total_amount_per_customer",
        "tables": ["sales"],
        "description": "Affiche le total des achats (amount) réalisés par chaque client (customer)."
    },
    {
        "theme": "window_functions",
        "exercise_name": "salary_ranking_by_department",
        "tables": ["employees"],
        "description": "Classe les employés de chaque département en fonction de leur salaire, du plus élevé au plus faible."
    },
    {
        "theme": "joins",
        "exercise_name": "users_and_purchases",
        "tables": ["users", "purchases"],
        "description": "Associe chaque utilisateur à son produit acheté, avec un FULL OUTER JOIN."
    },
    {
        "theme": "joins",
        "exercise_name": "inner_join_users_with_purchases",
        "tables": ["users", "purchases"],
        "description": "Affiche uniquement les utilisateurs ayant effectué un achat (INNER JOIN)."
    },
    {
        "theme": "joins",
        "exercise_name": "left_join_users_with_purchases",
        "tables": ["users", "purchases"],
        "description": "Affiche tous les utilisateurs, qu’ils aient acheté quelque chose ou non (LEFT JOIN)."
    },
    {
        "theme": "joins",
        "exercise_name": "left_join_purchases_with_users",
        "tables": ["users", "purchases"],
        "description": "Affiche tous les achats, même s’ils n’ont pas de client associé (LEFT JOIN inversé)."
    },
    {
        "theme": "joins",
        "exercise_name": "full_join_users_with_purchases",
        "tables": ["users", "purchases"],
        "description": "Montre toutes les correspondances entre utilisateurs et achats, y compris les cas sans correspondance des deux côtés (FULL OUTER JOIN)."
    },
]

default_date = "1970-01-01"
for ex in exercises:
    ex["last_reviewed"] = default_date

for ex in exercises:
    ex["tables"] = ",".join(ex["tables"])

memory_state_df = pd.DataFrame(exercises)
con.execute("CREATE OR REPLACE TABLE memory_state AS SELECT * FROM memory_state_df")

# ------------------------------------------------------------------------------
# TABLE CREATION
# ------------------------------------------------------------------------------

def create_table_from_csv(name, csv_string):
    df = pd.read_csv(io.StringIO(csv_string))
    con.execute(f"CREATE TABLE IF NOT EXISTS {name} AS SELECT * FROM df")

# Cross Join Tables
create_table_from_csv("beverages", """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
""")

create_table_from_csv("food_items", """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
""")

create_table_from_csv("sizes", """
size
XS
M
L
XL
""")

create_table_from_csv("trademarks", """
trademark
Nike
Asphalte
Abercrombie
Lewis
""")

# Group By Table
create_table_from_csv("sales", """
customer,product,amount
Alice,Apple,5
Alice,Banana,3
Bob,Apple,2
Bob,Orange,4
Charlie,Banana,1
Charlie,Orange,2
""")

# Window Functions Table
create_table_from_csv("employees", """
employee,department,salary
John,Sales,5000
Jane,Sales,6000
Doe,HR,4500
Anna,HR,4700
Chris,IT,5500
Eve,IT,5800
""")

# Join Tables
create_table_from_csv("users", """
id,name
1,Alice
2,Bob
3,Charlie
4,David
""")

create_table_from_csv("purchases", """
id,product
2,Book
3,Pen
5,Notebook
""")

con.close()
