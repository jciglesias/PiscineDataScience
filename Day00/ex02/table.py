import csv, psycopg2

if __name__=="__main__":
    conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
    conn.autocommit = False
    cursor = conn.cursor()

    tableName = "data_2022_oct"
    with open(f"/sgoinfre/goinfre/Perso/jiglesia/customer/data_2022_oct.csv", mode="r") as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {tableName.upper()}({header[0]} timestamp NOT NULL, {header[1]} text, {header[2]} int, {header[3]} float, {header[4]} integer, {header[5]} varchar);''')
        cursor.copy_from(csvfile, table=f"{tableName.lower()}", sep=',', columns=header)
    conn.commit()
    conn.close()
