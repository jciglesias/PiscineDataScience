import psycopg2

if __name__ == "__main__":
    conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
    conn.autocommit = True
    cursor = conn.cursor()

    # cursor.execute('''
    #                 SELECT customers.*, items.*
    #                FROM customers
    #                INNER JOIN items ON customers.product_id = items.product_id;
    #                ''')
    cursor.execute('''
                    ALTER TABLE customers
                    ADD COLUMN category_id varchar,
                    ADD COLUMN category_code VARCHAR,
                    ADD COLUMN brand VARCHAR;
                   ''')
    cursor.execute('''
                    UPDATE customers AS c
                    SET
                        category_id = i.category_id,
                        category_code = i.category_code,
                        brand = i.brand
                    FROM items AS i
                    WHERE c.product_id = i.product_id;
                    ''')
    cursor.close()
    conn.close()