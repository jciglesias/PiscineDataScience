import psycopg2, datetime
import matplotlib.pyplot as plt

if __name__ == "__main__":
    conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
    conn.autocommit = False
    cursor = conn.cursor()

    day = datetime.datetime(2022,10,1)
    count = {}
    while (day < datetime.datetime(2023,3,1)):
        cursor.execute(f"""
                       SELECT user_id, price
                       FROM customers 
                       WHERE event_time BETWEEN '{day.date()}' AND '{(day + datetime.timedelta(1)).date()}'
                       AND event_type = 'purchase'
                       """)
        query = cursor.fetchall()
        count[day] = len(query)
        day += datetime.timedelta(1)
    cursor.close()
    conn.close()
    
    plt.plot(count.keys(), count.values())
    plt.show()
