import streamlit as st
import psycopg2
import plotly.express as px
import pandas as pd
from sklearn.datasets import make_blobs

query = """
    SELECT 
        user_id,
        SUM(CASE WHEN event_type = 'purchase' THEN price ELSE 0 END) as total_spent,
        COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) as purchase_frequency
    FROM customers 
    WHERE category_id IS NOT NULL
    GROUP BY user_id
    HAVING COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) > 0
"""

st.set_page_config(page_title="elbow", page_icon=":bar_chart:", layout="wide")
conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
conn.autocommit = False
cursor = conn.cursor()

def get_data():
	cursor.execute(query)
	data = cursor.fetchall()
	return pd.DataFrame(data, columns=["user_id", "total_spent", "purchase_frequency"])

dataset = get_data()
x,y = make_blobs(n_samples=100, centers=3, cluster_std=0.60, random_state=0)
kmean_fig = px.scatter(x=x[:, 0], y=x[:, 1], title="K-means Clustering Example")
st.plotly_chart(kmean_fig, use_container_width=True)
