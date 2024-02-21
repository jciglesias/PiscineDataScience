import psycopg2

if __name__ == "__main__":
    conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute('''
                    DELETE FROM customers
                    WHERE (event_time, event_type, product_id, price, user_id, user_session) IN (
                        SELECT event_time, event_type, product_id, price, user_id, user_session
                        FROM customers
                        GROUP BY event_time, event_type, product_id, price, user_id, user_session
                        HAVING COUNT(*) > 1
                    );
                    ''')
    cursor.close()
    conn.close()