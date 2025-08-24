import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px

conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
conn.autocommit = False
cursor = conn.cursor()

query = """
with st_users as (
SELECT 
	user_id,
	SUM(CASE WHEN event_type = 'purchase' THEN price ELSE 0 END) as total_spent,
	COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) as purchase_frequency,
	max(case when event_type = 'purchase' then event_time end) as last_purchase
FROM customers 
WHERE category_id IS NOT NULL
GROUP BY user_id
)
select
	count(case when last_purchase < '11-01-2022' then 1 end) as inactive,
	count(case when purchase_frequency = 1 then 1 end) as new_customers,
	count(case when purchase_frequency > 1 then 1 end) as loyal_customers
from st_users
"""

def get_data():
	cursor.execute(query)
	data = cursor.fetchall()
	return pd.DataFrame(data, columns=["inactive", "new_customers", "loyal_customers"])

type_of_customer = get_data()
types_fig = px.bar(x=type_of_customer.columns, y=type_of_customer.iloc[0], title='Customer Types Distribution')
st.plotly_chart(types_fig, use_container_width=True)