import pandas as pd
from solver import solve_lp

substrate_names = ['S1', 'S2']

test_df = pd.DataFrame({
    'Biogas': [9, 10],
    'Weight': [60, 50],
    'Fat': [0.11, 0.08],
    'Cost': [2, 2],
    'Distance': [0, 0],
}, index=['S1', 'S2'], dtype=float)


print(solve_lp(test_df, 500, 10))