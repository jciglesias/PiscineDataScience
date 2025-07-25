import psycopg2

if __name__ == "__main__":
    conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute('''
                    DELETE FROM customers a
                    USING customers b
                    WHERE a.ctid > b.ctid
                    AND a.event_time = b.event_time
                    AND a.event_type = b.event_type
                    AND a.product_id = b.product_id
                    AND a.price = b.price
                    AND a.user_id = b.user_id
                    AND a.user_session = b.user_session;
                    ''')
    cursor.close()
    conn.close()