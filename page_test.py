import streamlit as st
import requests
import time

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


api_url = "http://egke.agro.auth.gr:8685/predict/"
get_prediction = st.button(
    "Πρόβλεψη", help="Get the prediction from the model")

if get_prediction:
    with st.spinner('Wait for it...'):
        try:
            response = requests.post(
                api_url, json=post_data, timeout=10)
            response.raise_for_status()
            data = response.json()
            print(data)
            st.table(data)
            st.success('Done!')
        except requests.exceptions.RequestException as errex:
            # st.write(errex)
            st.error('Error!')
