import psycopg2

if __name__=="__main__":
    conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS customers;')

    cursor.execute('''
                    CREATE TABLE customers AS
                    SELECT *
                    FROM data_2022_dec
                    UNION ALL
                    SELECT *
                    FROM data_2022_nov
                    UNION ALL
                    SELECT *
                    FROM data_2022_oct
                    UNION ALL
                    SELECT *
                    FROM data_2023_jan;
                    ''')
    cursor.close()
    conn.close()
