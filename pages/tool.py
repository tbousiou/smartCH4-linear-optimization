import streamlit as st
import pandas as pd
from solver import solve_lp


initial_df = pd.DataFrame({
    'Biogas': [9, 10],
    'Weight': [60, 50],
    'Fat': [0.11, 0.08],
    'Cost': [2, 2],
    'Distance': [0, 0],
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
    n = st.number_input('Ημέρες παραγωγής', value=10,
                        min_value=1, max_value=30)

with col3:
    error_pct = st.number_input('Απόκλιση στόχου (%)', value=0,
                                min_value=0, max_value=30, help='Do not use!')

multiple_targets_help_text = """
Επιλέγοντας αυτή την επιλογή η εφαρμογή θα διερευνήσει λύσεις για διάφορες τιμές γύρω από τον στόχο παραγωγής μεθανίου.
"""
multiple_targets = st.checkbox(
    'Διευρεύνση λύσεων κοντά στο στόχο?', key='many_solutions', help=multiple_targets_help_text)

total_target = target*n
deviation = (total_target*error_pct) / 100
st.write(f"Βασικός στόχος παραγωγής για {n} ημέρες: {total_target} ± {deviation:.2f}")

"""
Κάντε κλικ στο κουμπί **SOLVE** για να υπολογιστούν οι λύσεις.
Αν δε βρεθεί μια λύση σημαίνει ότι οι περιορισμοί δεν είναι εφικτοί.
Προσέξτε ότι υπάρχει περιπτώσεις μια λύση να είναι βέλτιση αλλά όχι η μοναδική. Αυτό μπορεί να συμβει π.χ. αν τα υποστρώματα έχουν τα ίδια χαρακτηριστικά.
"""

# Add a button to solve the linear programming problem
if st.button('Solve LP'):
    if multiple_targets:
        test_target_deviations = [-10, -5, -2, 0, 2, 5, 10]
    else:
        test_target_deviations = [0]

    for i in test_target_deviations:

        test_target = total_target + (i/100)*total_target

        solution = solve_lp(current_df, test_target, deviation)
        if solution:
            st.success(f"Βρέθηκε βέλτιση λύση για στόχο {test_target}", icon="✅")
            st.write(f"Κόστος {solution['objective (cost)']:.2f} Ευρώ")

            total_fat = current_df['Fat'] @ pd.Series(solution['solution'])
            total_fat_percentage = total_fat / current_df['Weight'].sum()
            st.write(f"Συνολικό ποσοστό λίπους: {100 * total_fat_percentage:.2f} %")

            st.write('Βέλτιστη σύνθεση μίγματος σε Kg:')
            st.table(solution['solution'])
        else:
            st.error(f"Δε βρέθηκε βέλτιση λύση για στόχο {test_target}! Ελέγξτε τους περιορισμούς.")

        st.divider()
