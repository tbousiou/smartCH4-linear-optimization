import streamlit as st
import pandas as pd
from solver import solve_lp


initial_df = pd.DataFrame({
        'B': [10, 10],
        'W': [50, 50],
        'F': [0.1, 0.15],
        'C': [2, 2],
        'D': [0, 0],
    }, index=['S1', 'S2'], dtype=float)


if st.session_state.get('df') is None:
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
"""
Στον πίνακα υποστρωμάτων συμπληρώστε τιμές. Αν χρειαστεί προσθέστε νέα γραμμή με κλικ στη κάτω σειρά ή διαγράφετε γραμμή με κλικ στην αριστερή άκρη.
"""

current_df = st.data_editor(st.session_state.df, num_rows="dynamic")

"""
Εδώ επιλέξετε τις βασικές παραμέτρους για τον υπολογισμό της βέλτιστης λύσης.
"""

col1, col2, col3 = st.columns(3)
with col1:
    target = st.number_input('Ημερήσια παραγωγή μεθανίου (T)',
                value=100, min_value=10, max_value=1000)
with col2:
    error_pct =  st.number_input('Απόκλιση στόχου (%)', value=0,
                min_value=0, max_value=30)
with col3:
    n = st.number_input('Ημέρες παραγωγής', value=10, min_value=1, max_value=30)

total_target = target*n
deviation = (total_target*error_pct) / 100
st.write(f'Στόχος παραγωγής για {n} ημέρες: {total_target} ± {deviation:.2f}')

"""
Κάντε κλικ στο κουμπί **SOLVE** για να υπολογιστεί η λύση. Αν δε βρεθεί λύση σημαίνει ότι οι περιορισμοί δεν είναι εφικτοί.
Προσέξτε ότι όταν υπάρχουν πολλές λύσεις ο αλγόριμθμος επιλέγει την πρώτη που βρίσκει. Αυτό μπορεί να συμβει π.χ. αν τα υποστρώματα έχουν τα ίδια χαρακτηριστικά.
"""

# Add a button to solve the linear programming problem
if st.button('Solve LP'):
    solution = solve_lp(current_df, total_target, deviation)
    if solution:
        st.success('Βρέθηκε βέλτιση λύση:!', icon="✅")
        st.write(f"Κόστος {solution['objective (cost)']} Ευρώ")
        st.write('Βέλτιστη σύνθεση μίγματος σε Kg:')
        st.table(solution['solution'])
    else:
        st.error('Δε βρέθηκε βέλτιση λύση! Ελέγξτε τους περιορισμούς.')
