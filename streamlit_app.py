import streamlit as st

home_page = st.Page("page_home.py", title="Home", icon="🏠")
tool_page = st.Page("page_tool.py", title="LP tool", icon="🛠️")

pg = st.navigation([home_page, tool_page])
pg.run()
