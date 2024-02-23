import psycopg2

if __name__ == "__main__":
    conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
    conn.autocommit = False
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
                        category_id = i.max_category_id,
                        category_code = i.max_category_code,
                        brand = i.max_brand
                    FROM (
                        SELECT
                            product_id,
                            MAX(category_id) AS max_category_id,
                            MAX(category_code) AS max_category_code,
                            MAX(brand) AS max_brand
                        FROM items
                        GROUP BY product_id
                    ) AS i
                    WHERE c.product_id = i.product_id;
                    ''')
    cursor.close()
    conn.commit()
    conn.close()