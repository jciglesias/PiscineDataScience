import psycopg2, datetime
import plotly.express as px
import streamlit as st
from pandas import DataFrame

st.set_page_config(layout="wide")
conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
conn.autocommit = False
cursor = conn.cursor()

months = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}
def get_customers():
    cursor.execute("""
        SELECT DATE(event_time) as day, count(distinct user_id)
        FROM customers 
        WHERE event_type = 'purchase'
        group by day
		ORDER BY day
        """)

    data = cursor.fetchall()
    return data

def get_sales():
    cursor.execute("""
            SELECT 
                extract(month from DATE(event_time)) as month,
                sum(price) as sales
            FROM customers 
            WHERE event_type = 'purchase'
            group by month
            ORDER BY month
            """)

    data = DataFrame(cursor.fetchall(), columns=['month', 'total sales in million of ₳'])
    data['month'] = data['month'].apply(lambda x: months[int(x)])
    return data

def get_spent_per_day():
    cursor.execute("""
                with daily_user as(
                SELECT 
                    DATE(event_time) as days,
                    user_id,
                    sum(price) as spent
                FROM customers 
                WHERE event_type = 'purchase'
                group by days, user_id
                ORDER BY days
                )
                select
                    days,
                    avg(spent) as mean_spent
                from daily_user
                group by days
                order by days
                   """)

    data = cursor.fetchall()
    return data

c1, c2, c3 = st.columns(3)
data = DataFrame(get_customers(), columns=['day', 'number of customers'])
line_fig = px.line(
    data,
    x='day',
    y='number of customers',
    title='Number of Customers per Day',
)
line_fig.update_xaxes(title_text='')
c1.plotly_chart(line_fig)

bars_fig = px.bar(
    get_sales(),
    x='month',
    y='total sales in million of ₳',
    title='Monthly Sales'
)
bars_fig.update_xaxes(title_text='')
c2.plotly_chart(bars_fig)

spent_data = DataFrame(get_spent_per_day(), columns=['day', 'average spend/customers in ₳'])
spent_fig = px.line(
    spent_data,
    x='day',
    y='average spend/customers in ₳',
    title='Average Spent per Customer per Day'
)
spent_fig.update_traces(fill='tozeroy')
spent_fig.update_xaxes(title_text='')
c3.plotly_chart(spent_fig)

cursor.close()
conn.close()