import psycopg2
import matplotlib.pyplot as plt

if __name__ == "__main__":
    conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
    conn.autocommit = False
    cursor = conn.cursor()

    cursor.execute("SELECT event_type FROM customers")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    events = [row[0] for row in data]
    count  = {event: events.count(event) for event in set(events)}
    plt.pie(count.values(), labels=count.keys(), autopct='%1.1f%%')
    plt.show()

