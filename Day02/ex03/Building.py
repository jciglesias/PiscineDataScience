import psycopg2
import streamlit as st
import plotly.express as px

spent_query = """
with spent_customer as (
SELECT
	user_id,
	sum(price) as spent
FROM customers 
WHERE event_type = 'purchase'
group by user_id
)
select
	count(case when spent >=0 and spent < 50 then 1 else null end) as zero,
	count(case when spent >= 50 and spent < 100 then 1 else null end) fifty,
	count(case when spent >= 100 and spent < 150 then 1 else null end) hundred,
	count(case when spent >= 150 and spent < 200 then 1 else null end) hundredfifty,
	count(case when spent >= 200 then 1 else null end) twohundred
from spent_customer
"""

freq_query = """
with daily_user as(
SELECT 
	DATE(event_time) as days,
	user_id
FROM public.data_2022_dec 
WHERE event_type = 'purchase'
group by days, user_id
), freq as (
select
	user_id,
	count(user_id) as f
from daily_user
group by user_id)
select
	count(case when f < 5 then 1 else null end) as zero,
	count(case when f >= 5 and f < 10 then 1 else null end) as five,
	count(case when f >= 10 and f < 15 then 1 else null end) as ten,
	count(case when f >= 15 then 1 else null end) as fifteen
from freq
"""