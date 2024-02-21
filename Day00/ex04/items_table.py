import csv, psycopg2

if __name__=="__main__":
    conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
    conn.autocommit = False
    cursor = conn.cursor()

    tableName = "items"
    with open(f"/sgoinfre/goinfre/Perso/jiglesia/item/item.csv", mode="r") as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {tableName.upper()}({header[0]} int NOT NULL, {header[1]} varchar, {header[2]} varchar, {header[3]} varchar);''')
        cursor.copy_from(csvfile, table=f"{tableName.lower()}", sep=',', columns=header)
    conn.commit()
    conn.close()
