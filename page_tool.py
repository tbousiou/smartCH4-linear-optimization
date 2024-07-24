import streamlit as st
import pandas as pd
from solver import solve_lp
import random
import requests

api_url = "http://egke.agro.auth.gr:8685/predict/"
post_data = {
    "future": [
        10.6,
        1
    ],
    "past": [
        [
            8.87,
            1,
            6.91
        ],
        [
            11.02,
            1,
            10.83
        ],
        [
            9.46,
            1,
            10.89
        ],
        [
            11.93,
            1,
            10.95
        ],
        [
            10.89,
            1,
            10.96
        ],
        [
            11.01,
            1,
            10.98
        ]
    ]
}

@st.experimental_fragment
def get_prediction(key=None):
    col1, col2, col3 = st.columns(3)
    with col1:
        get_prediction_btn = st.button("Πρόβλεψη", help="Get the prediction from the model", key=key, type="secondary")
    with col2:
        if get_prediction_btn:
            with st.spinner('Wait for it...'):
                post_data['future'][0] = random.uniform(8, 18)
                post_data['future'][1] = random.uniform(0.5, 1.5)
                try:
                    response = requests.post(
                        api_url, json=post_data, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    st.table(data)
                    st.success('Done!')
                except requests.exceptions.RequestException as errex:
                    # st.write(errex)
                    st.error('Error!')
    with col3:            
        if get_prediction_btn:
            st.button("Save", help="Save the prediction to the database", type="primary")

initial_df = pd.DataFrame({
    'Methane': [9, 10],
    'Weight': [45, 35],
    'Fat': [0.11, 0.08],
    'Cost': [2.5, 2],
    'Distance': [1, 1],
}, index=['S1', 'S2'], dtype=float)


if st.session_state.get('df') is None:
    current_df = initial_df
    st.session_state.df = current_df


st.header('Υπολογισμός βέλτισης λύσης', divider='rainbow')
"""
Στον πίνακα υποστρωμάτων συμπληρώστε τιμές. Αν χρειαστεί προσθέστε νέα γραμμή με κλικ στη κάτω σειρά ή διαγράφετε γραμμή με κλικ στην αριστερή άκρη.
"""

current_df = st.data_editor(st.session_state.df, num_rows="dynamic")

"""
Εδώ επιλέξετε τις βασικές παραμέτρους για τον υπολογισμό της βέλτιστης λύσης.
"""

col1, col2 = st.columns(2)
with col1:
    target = st.number_input('Ημερήσια παραγωγή μεθανίου (T)',
                             value=100, min_value=10, max_value=1000)

with col2:
    n = st.number_input('Ημέρες παραγωγής', value=7,
                        min_value=1, max_value=30)



multiple_targets_help_text = """
Επιλέγοντας αυτή την επιλογή η εφαρμογή θα διερευνήσει λύσεις για διάφορες τιμές γύρω από τον στόχο παραγωγής μεθανίου.
"""
multiple_targets = st.checkbox(
    'Διευρεύνση λύσεων κοντά στο στόχο?', key='many_solutions', help=multiple_targets_help_text)

total_target = target*n

st.write(f"Βασικός στόχος παραγωγής CH4 για {n} ημέρες: {total_target} Liters")

"""
Κάντε κλικ στο κουμπί **SOLVE** για να υπολογιστούν οι λύσεις.
Αν δε βρεθεί μια λύση σημαίνει ότι οι περιορισμοί δεν είναι εφικτοί.
Προσέξτε ότι υπάρχει περιπτώσεις μια λύση να είναι βέλτιση αλλά όχι η μοναδική. Αυτό μπορεί να συμβει π.χ. αν τα υποστρώματα έχουν τα ίδια χαρακτηριστικά.
"""

# Add a button to solve the linear programming problem
if st.button('Solve LP', type="primary"):
    if multiple_targets:
        test_target_deviations = [-10, -5, -2, 0, 2, 5, 10]
    else:
        test_target_deviations = [0]

    for i in test_target_deviations:

        test_target = total_target + (i/100)*total_target

        solution = solve_lp(current_df, test_target, 0)
        if solution:
            st.success(f"Βρέθηκε βέλτιση λύση για στόχο {test_target}", icon="✅")
            st.write(f"Κόστος {solution['cost']:.2f} Ευρώ")

            total_fat = current_df['Fat'] @ pd.Series(solution['solution'])
            total_fat_percentage = total_fat / current_df['Weight'].sum()
            st.write(f"Συνολικό ποσοστό λίπους: {100 * total_fat_percentage:.2f} %")

            st.write('Βέλτιστη σύνθεση μίγματος σε Kg:')
            st.table(solution['solution'])
            get_prediction(key=i)
        else:
            st.error(f"Δε βρέθηκε βέλτιση λύση για στόχο {test_target}! Ελέγξτε τους περιορισμούς.")

        st.divider()
