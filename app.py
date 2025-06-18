# pylint: disable=missing-module-docstring
import os
import logging
from datetime import date, timedelta

import duckdb
import streamlit as st

# Setup database
if "data" not in os.listdir():
    logging.debug("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# Functions
def check_users_solution(user_query: str) -> None:
    result = con.execute(user_query).df()
    st.dataframe(result)
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
        if result.compare(solution_df).shape == (0, 0):
            st.write('Correct !')
            st.balloons()
    except KeyError:
        st.write("Some columns are missing")

    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(f"result has a {n_lines_difference} lines difference with the solution_df")

# Sidebar
with st.sidebar:
    available_themes_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    theme_list = available_themes_df["theme"].dropna().unique().tolist()
    theme_list.insert(0, "– Tous les thèmes –")

    # Initialisation dans session_state
    if "selected_theme" not in st.session_state:
        st.session_state.selected_theme = "– Tous les thèmes –"

    # Menu déroulant piloté par session_state
    selected = st.selectbox(
        "What would you like to review?",
        theme_list,
        index=theme_list.index(st.session_state.selected_theme),
        key="selected_theme"
    )

    # Charger les exercices selon le thème sélectionné
    if selected == "– Tous les thèmes –":
        select_exercise_query = "SELECT * FROM memory_state"
    else:
        select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{selected}'"

    exercise = (
        con.execute(select_exercise_query)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )

    if exercise.empty:
        st.warning("Aucun exercice trouvé pour ce thème.")
        st.stop()

    st.write("Liste des exercices disponibles :")
    st.dataframe(exercise)

    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

# Main Interface
st.header("Enter your SQL code")

st.subheader("Énoncé de l'exercice :")
st.write(exercise.loc[0, "description"])

query = st.text_area(label="Votre code SQL ici", key="user_input")

if query:
    check_users_solution(query)

# Buttons
for n_days in [2, 7, 21]:
    if st.button(f"Revoir dans {n_days} jours"):
        next_review = date.today() + timedelta(days=n_days)
        con.execute(f"""
            UPDATE memory_state 
            SET last_reviewed = '{next_review}' 
            WHERE exercise_name = '{exercise_name}'
        """)
        st.rerun()

if st.button("Reset"):
    con.execute("UPDATE memory_state SET last_reviewed = '1970-01-01'")
    st.rerun()

# Tabs
tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    exercise_tables = exercise.loc[0, "tables"].split(",")
    for table in exercise_tables:
        st.write(f"Table: {table}")
        df_tables = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_tables)

with tab3:
    st.text(answer)

