import streamlit as st
import pandas as pd
from solver import solve_lp


initial_df = pd.DataFrame({
        'B': [11, 10],
        'W': [40, 20],
        'C': [3, 2],
        'D': [0, 0],
    }, index=['S1', 'S2'], dtype=float)


if st.session_state.get('df') is None:
    st.write('Initializing session state')
    current_df = initial_df
    st.session_state.df = current_df

# substrate_names = ['S1', 'S2']

# df = pd.DataFrame({
#     'B': [10, 10],
#     'W': [40, 20],
#     'C': [3, 2],
#     'D': [0, 0],
# }, index=substrate_names, dtype=float)

st.header('Υπολογισμός βέλτισης λύσης', divider='rainbow')
st.subheader('Δεδομένα υποσρτωμάτων')

current_df = st.data_editor(st.session_state.df, num_rows="dynamic")

col1, col2 = st.columns(2)
with col1:
    target = st.number_input('Στόχος παραγωγής μεθανίου (T)',
                value=500, min_value=50, max_value=1000)
with col2:
    error_pct =  st.number_input('Απόκλιση στόχου (%)', value=.0,
                min_value=0.0, max_value=0.3)


# Add a button to solve the linear programming problem
if st.button('Solve LP'):
    solution = solve_lp(current_df, target, error_pct)
    if solution:
        st.write('Βρέθηκε βέλτιση λύση:')
        st.write(f"Κόστος {solution['objective (cost)']}")
        st.table(solution['solution'])
    else:
        st.write('Δε βρέθηκε βέλτιση λύση. Ελέγξτε τους περιορισμούς.')
