import psycopg2

if __name__ == "__main__":
    conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute('''
                    DELETE FROM customers c1
                    WHERE EXISTS (
                        SELECT 1 FROM customers c2
                        WHERE c2.event_type = c1.event_type
                        AND c2.product_id = c1.product_id
                        AND c2.user_id = c1.user_id
                        AND c2.user_session = c1.user_session
                        AND c2.price = c1.price
                        AND ABS(EXTRACT(EPOCH FROM (c2.event_time - c1.event_time))) <= 1
                        AND c2.event_time < c1.event_time
                    );
                    ''')
    cursor.close()
    conn.close()