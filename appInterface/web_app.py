import os
import streamlit as st
import pandas as pd
import requests

st.title("User Movie Recommendations")
name = st.text_input("Your Name", key="name")

model_ip = os.environ.get("MODEL_IP", "basemodel")
model_port = os.environ.get("MODEL_PORT", "8000")

def load_data(name: str):
    response = requests.post(f"http://{model_ip}:{model_port}/recommendations", json={"user": name})
    json_response = response.json()
    if json_response["status"] == 200:
        return pd.DataFrame(json_response["response"])
    else:
        return pd.DataFrame(
            {
                "Ranking": [1, 2, 3, 4, 5],
                "Movies": ["Avengers: Endgame", "Avengers: Infinity War", "Captain America: The Winter Soldier", "Iron Man", "Thor: Ragnarok"],
            }
        )

if name:
    df = load_data(name)
    st.dataframe(df, hide_index=True, use_container_width=False)
else:
    st.text("Type your User ID to retrieve recommended movies")