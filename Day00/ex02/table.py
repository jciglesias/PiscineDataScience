import os, csv, psycopg2, threading

filepath = "/sgoinfre/goinfre/Perso/jiglesia/customer"

def tables(file: str):
    conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
    conn.autocommit = False
    cursor = conn.cursor()

    tableName = file.replace(".csv", "")
    with open(f"{filepath}/{file}", mode="r") as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {tableName.upper()}({header[0]} timestamp NOT NULL, {header[1]} varchar(50), {header[2]} int, {header[3]} float, {header[4]} int, {header[5]} varchar(100));''')
        cursor.copy_from(csvfile, table=f"{tableName.lower()}", sep=',', columns=header)
    conn.commit()
    conn.close()

if __name__=="__main__":
    files = os.listdir(filepath)
    threads = []
    for file in files:
        threads.append(threading.Thread(target=tables, args=(file,)))
    for t in threads:
        t.start()
    for th in threads:
        th.join()
