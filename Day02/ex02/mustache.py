import streamlit as st
import plotly.express as px
import pandas as pd
import psycopg2

st.set_page_config(page_title="Mustache Store", page_icon=":bar_chart:", layout="wide")
conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
conn.autocommit = False
cursor = conn.cursor()
def get_stats():
    query = """
        SELECT 
            count(*),
            avg(price) as mean,
            stddev_pop(price) as std,
            percentile_cont(0) within group (order by price) as minimum,
            percentile_cont(0.25) within group (order by price) as p25,
            percentile_cont(0.5) within group (order by price) as p50,
            percentile_cont(0.75) within group (order by price) as p75,
            percentile_cont(1) within group (order by price) as maximum
        FROM public.customers
        where event_type = 'purchase'
        """

    cursor.execute(query)
    result = cursor.fetchall()
    # return result
    return pd.DataFrame(result, columns=["count", "mean", "std", "minimum", "p25", "p50", "p75", "maximum"])

@st.cache_data()
def get_data():
    query = """
        SELECT price FROM public.customers
        where event_type = 'purchase'
        order by price
        """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=["price"])

@st.cache_data()
def get_avg_basket():
    query = """
        with daily_user as(
        SELECT 
            DATE(event_time) as days,
            user_id,
            sum(price) as spent
        FROM customers 
        WHERE event_type = 'cart'
        group by days, user_id
        ORDER BY days
        )
        select
            user_id,
            avg(spent) as avg_basket
        from daily_user
        group by user_id
        order by avg_basket 
        """
    
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=["user_id", "avg_basket"])

stats = get_stats()
st.dataframe(stats, hide_index=True)

data = get_data()
box_fig = px.box(data, x="price", title="Box Plot of Prices")
st.plotly_chart(box_fig, use_container_width=True)

basket_data = get_avg_basket()
basket_fig = px.box(basket_data, x="avg_basket", title="Average Basket per User")
st.plotly_chart(basket_fig, use_container_width=True)
