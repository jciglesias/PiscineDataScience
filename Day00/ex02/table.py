import os, csv, tqdm, psycopg2, threading

filepath = "/sgoinfre/goinfre/Perso/jiglesia/customer"
totalLines = {
    "data_2022_dec.csv": 3533287,
    "data_2022_nov.csv": 4635838,
    "data_2022_oct.csv": 4102284,
    "data_2023_jan.csv": 4264753
}

def tables(file: str):
    conn = psycopg2.connect(database="piscineds", user='jiglesia', password='mysecretpassword', host='127.0.0.1')
    cursor = conn.cursor()

    conn.autocommit = False
    tableName = file.replace(".csv", "")
    with open(f"{filepath}/{file}", mode="r") as csvfile:
        csvreader = csv.reader(csvfile)
        headder = next(csvreader)
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {tableName.upper()}({headder[0]} timestamp NOT NULL, {headder[1]} varchar(50), {headder[2]} int, {headder[3]} float, {headder[4]} int, {headder[5]} varchar(100));''')
        cursor.copy_from(csvfile, table=f"{tableName.lower()}", sep=',', columns=headder)
        # values = []
        # i = 0
        # for row in tqdm.tqdm(csvreader, desc=f"{tableName}: ",total=totalLines[file]):
        #     # cursor.executemany(f'INSERT INTO {tableName.lower()} VALUES(%s,%s,%s,%s,%s,%s)', [(f'{row[0].replace(" UTC", "")}',f'{row[1]}',f'{row[2]}',f'{row[3]}',f'{row[4]}',f'{row[5]}')])
        #     i += 1
        #     values.append((f'{row[0].replace(" UTC", "")}',f'{row[1]}',f'{row[2]}',f'{row[3]}',f'{row[4]}',f'{row[5]}'))
        #     if i == 30000:
        #         cursor.executemany(f'INSERT INTO {tableName.lower()} VALUES(%s,%s,%s,%s,%s,%s)', values)
        #         i = 0
        #         values.clear()
        # if len(values):
        #     cursor.executemany(f'INSERT INTO {tableName.lower()} VALUES(%s,%s,%s,%s,%s,%s)', values)
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
