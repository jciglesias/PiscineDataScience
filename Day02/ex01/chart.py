import psycopg2, datetime
import matplotlib.pyplot as plt

if __name__ == "__main__":
    conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
    conn.autocommit = False
    cursor = conn.cursor()

    # cursor.execute("SELECT event_time, price, user_id FROM customers WHERE event_type = 'purchase'")
    day = datetime.datetime(2022,10,1)
    count = {}
    while (day < datetime.datetime(2023,3,1)):
        cursor.execute(f"SELECT user_id FROM customers WHERE event_type = 'purchase' AND event_time = {day.date()}")
        count[day] = len(cursor.fetchall())
        day += datetime.timedelta(1)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # time, price, user = zip(*data)
    plt.plot(count.keys(), count.values())
    plt.show()
