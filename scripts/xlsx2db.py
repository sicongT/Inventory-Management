# coding=utf-8
import pandas as pd
import sqlite3
import os


def createDb(dbname, tablename, headers):
    connect = sqlite3.connect(dbname)
    c = connect.cursor()
    sql = '''create table {table_name}
    (id integer primary key autoincrement,
     {产品名称} text not null,
     {产品编号} char(50) not null,
     {产品金额} int not null,
     {库存数量} int,
     {数量范围} char(50),
     {剩余容量} int);
     '''.format(table_name=tablename, 产品名称=headers[0], 产品编号=headers[1], 产品金额=headers[2], 库存数量=headers[3],
                数量范围=headers[4], 剩余容量=headers[5])
    print(sql)
    c.execute(sql)
    connect.commit()
    c.close()
    connect.close()
    print("Database created!")

def insertDb(db, headers, tablename, dbname):
    connect = sqlite3.connect(dbname)
    c = connect.cursor()
    sql_base = '''insert into {table_name} ({产品名称},{产品编号},{产品金额},{库存数量},{数量范围})'''.format(table_name=tablename,
                                                                                          产品名称=headers[0],
                                                                                          产品编号=headers[1],
                                                                                          产品金额=headers[2],
                                                                                          库存数量=headers[3],
                                                                                          数量范围=headers[4])
    for i in range(len(db[headers[0]])):
        row = []
        for j in range(len(headers)):
            row.append(db[headers[j]][i])
        sql = sql_base + '''values ('{}','{}','{}','{}','{}');'''.format(row[0], row[1], row[2], row[3], row[4])
        print(sql)
        c.execute(sql)
        connect.commit()
    c.close()
    connect.close()
    print("Data inserted!")

def checkDb(dbname, tablename):
    connect = sqlite3.connect(dbname)
    c = connect.cursor()
    sql = "select * from {table}".format(table=tablename)
    print(sql)
    res = c.execute(sql)
    for row in res:
        print(row)
    c.close()
    connect.close()

def Dbgen_fromexcel(xlsx_path, dbname, tablename):
    data = pd.read_excel(xlsx_path)
    headers = data.columns
    if not os.path.isfile(dbname):
        createDb(dbname, tablename, headers)
    insertDb(data, headers, tablename, dbname)
    checkDb(dbname, tablename)
    print("Database generated!")


xlsx_path = "数据.xlsx"
Dbgen_fromexcel(xlsx_path, "../库存.db", "库存清单")
