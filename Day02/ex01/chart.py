import psycopg2, datetime
import matplotlib.pyplot as plt
from statistics import mean

if __name__ == "__main__":
    conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
    conn.autocommit = False
    cursor = conn.cursor()

    day = datetime.datetime(2022,10,1)
    data = {}
    while (day < datetime.datetime(2023,2,1)):
        cursor.execute(f"""
                       SELECT user_id, price
                       FROM customers 
                       WHERE event_time BETWEEN '{day.date()}' AND '{(day + datetime.timedelta(1)).date()}'
                       AND event_type = 'purchase'
                       """)
        query = cursor.fetchall()
        data[day] = {"count": len(query), "id": [], "price": []}
        for x in query:
            data[day]["id"].append(x[0])
            data[day]["price"].append(x[1])
        day += datetime.timedelta(1)
    cursor.close()
    conn.close()
    ax1: plt.Axes
    ax2: plt.Axes
    ax3: plt.Axes
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)
    
    ax1.plot(data.keys(), [x["count"] for x in data.values()])
    ax1.set_title('Customers per day')
    ax1.set_xlabel('Days')
    ax1.set_ylabel('Number of customers')
    plt.setp(ax1.get_xticklabels(), rotation=45)
    
    t_sales = [[],[],[],[]]
    for x in data:
        if x.month == 10:
            t_sales[0].append(sum(data[x]["price"]))
        elif x.month == 11:
            t_sales[1].append(sum(data[x]["price"]))
        elif x.month == 12:
            t_sales[2].append(sum(data[x]["price"]))
        elif x.month == 1:
            t_sales[3].append(sum(data[x]["price"]))
    ax2.bar(["oct", "nov", "dec", "jan"], [sum(x) for x in t_sales])
    ax2.set_title('Income per month')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Income ₳')

    avg = {}
    for x in data:
        avg[x] = dict.fromkeys(data[x]["id"])
        for client in avg[x]:
            avg[x][client] = []
        for i in range(len(data[x]["id"])):
            avg[x][data[x]["id"][i]].append(data[x]["price"][i])
    for x in avg:
        for client in avg[x]:
            avg[x][client] = sum(avg[x][client])
        avg[x] = mean(avg[x].values())
    ax3.plot(avg.keys(), avg.values(), color='blue')
    ax3.fill_between(avg.keys(), avg.values(), color='lightblue')
    ax3.set_title('Average spent per customer per day')
    ax3.set_xlabel('Days')
    ax3.set_ylabel('Spent per day')
    plt.setp(ax3.get_xticklabels(), rotation=45)

    ax4.axis("off")

    plt.tight_layout()
    plt.show()
