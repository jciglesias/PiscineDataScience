import psycopg2
import plotly.express as px
import streamlit as st

@st.cache_data
def get_data():
    conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
    conn.autocommit = False
    cursor = conn.cursor()

    cursor.execute("SELECT event_type, COUNT(*) FROM customers GROUP BY event_type")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

data = get_data()
event_types, counts = zip(*data)
fig = px.pie(names=event_types, values=counts, title='Event Type Distribution')
st.plotly_chart(fig)
