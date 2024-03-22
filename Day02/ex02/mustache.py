import psycopg2, datetime
import matplotlib.pyplot as plt
import statistics as sts

# def meanCart(data: dict):
#     avg = {}
#     for x in data:
#         avg[x] = dict.fromkeys(data[x]["id"])
#         for client in avg[x]:
#             avg[x][client] = []
#         for i in range(len(data[x]["id"])):
#             if data[x]["event"][i] == "cart":
#                 avg[x][data[x]["id"][i]].append(data[x]["price"][i])
#             else:
#                 avg[x][data[x]["id"][i]].remove(data[x]["price"][i])


if __name__ == "__main__":
    conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
    conn.autocommit = False
    cursor = conn.cursor()
    # cursor.execute(f"""
    #                 SELECT price
    #                 FROM customers
    #                 WHERE event_type = 'purchase'
    #                 """)
    # prices = [x[0] for x in cursor.fetchall()]
    
    # day = datetime.datetime(2022,10,1)
    data = {}
    # while (day < datetime.datetime(2023,2,1)):
        # cursor.execute(f"""
        #                SELECT user_id, price, event_type, product_id
        #                FROM customers 
        #                WHERE event_time BETWEEN '{day.date()}' AND '{(day + datetime.timedelta(1)).date()}'
        #                AND (event_type = 'cart' OR event_type = 'remove_from_cart')
        #                """)
    cursor.execute(f"""
                   SELECT user_id, price
                   FROM customers 
                   WHERE event_type = 'purchase'
                   """)
    query = cursor.fetchall()
    # data[day] = {}
    for x in query:
        if x[0] not in data:
            data[x[0]] = []
        # if x[2] == "cart":
        data[x[0]].append(x[1])
            # elif x[2] == "remove_from_cart":
            #     try:
            #         data[day][x[0]].remove(x[1])
            #     except:
            #         pass
        # day += datetime.timedelta(1)

    # cursor.close()
    # conn.close()
    # print(f"count\t{len(prices)}")
    # print(f"mean\t{sts.mean(prices)}")
    # print(f"median\t{sts.median(prices)}")
    # print(f"std\t{sts.pstdev(prices)}")
    # print(f"min\t{min(prices)}")
    # prices.sort()
    # print(f"25%\t{prices[int(len(prices)*0.25)]}")
    # print(f"50%\t{prices[int(len(prices)*0.5)]}")
    # print(f"75%\t{prices[int(len(prices)*0.75)]}")
    # print(f"max\t{max(prices)}")

    ax1: plt.Axes
    ax2: plt.Axes
    ax3: plt.Axes
    fig, ((ax1), (ax2), (ax3)) = plt.subplots(3,1)
    # ax1.boxplot(prices, vert=False, widths=0.8)
    # ax2.boxplot(prices, vert=False, widths=0.8, showfliers=False, patch_artist=True, boxprops=dict(facecolor="lightgreen", color="green"))
    cart_price = []
    for x in data:
        # for y in data[x]:
        cart_price.append(sum(data[x]))
    ax3.boxplot([x for x in cart_price if x != 0], vert=False, widths=0.8)
    plt.tight_layout()
    plt.show()

