import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

@st.cache_resource
def load_data():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    store_names = ["Arora store", "Bharti store", "Tiwari general Store", "Dadi general store", "Dhiman general store"]
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1PtuPiSfGcBMY8lEeD2FCKHGUJAqUgQyDW9hF_fwOy8c/edit")

    data = {}
    for store in store_names:
        df = pd.DataFrame(sheet.worksheet(store).get_all_records())
        df.columns = [col.strip() for col in df.columns]  # Clean column headers
        data[store] = df
    return data
