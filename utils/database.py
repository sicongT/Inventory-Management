import sqlite3
import os
import sys

class Database:
    def __init__(self):
        dataset_name = "库存.db"

        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)
            application_path = os.path.dirname(application_path)

        self.db_dir = os.path.join(application_path, dataset_name)
        self.table = "库存清单"
        self.data = None
        self.cols = None

    def get_data(self):
        return self.data

    def get_header_name(self):
        return self.cols

    def get_row_num(self):
        return len(self.data)

    def get_col_num(self):
        return len(self.data[0])

    def row_info(self, keys=None):
        '''
        It is used to illustrate the specific row in the table if the variable key is given by user, otherwise all data
        in this table will be given.
        :param keys: list: key info of that row
        :return: all data or data lines
        '''
        if self.data:
            rows = []
            if keys:
                for row in self.data:
                    for key in keys:
                        if key in row:
                            rows.append(row)
                return rows
        return self.data

    def col_info(self, keys=None):
        connect = sqlite3.connect(self.db_dir)
        c = connect.cursor()
        col_info_sql = self._sql_gen("5", keys)
        col_info = [col for col in c.execute(col_info_sql)]
        connect.commit()
        c.close()
        connect.close()
        return col_info

    def loading(self, db_path="库存.db", tablename="库存清单"):

        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)
            application_path = os.path.dirname(application_path)

        self.db_dir = os.path.join(application_path, db_path)

        self.table = tablename
        connect = sqlite3.connect(self.db_dir)
        c = connect.cursor()
        data_sql = self._sql_gen("0")
        if self._check_sql(data_sql):
            self.data = [list(row) for row in c.execute(data_sql)]
            self.cols = [tuple[0] for tuple in c.description]
            connect.commit()
        c.close()
        connect.close()
        self.checkrest()

    def info(self):
        info = self.row_info()
        if info:
            print("---------{}----------".format(self.table))
            for item in info:
                print(" ".join(map(str, item)))
        else:
            print("Dataset {} is empty! Please load {} or check {}'s data first!".format(self.table, self.table,
                                                                                         self.table))

    def _check_sql(self, sql):
        return bool(sql)

    def _sql_gen(self, func=None, key=None):
        if func == "0":
            sql = "select * from {table}".format(table=self.table)
        elif func == "1":
            sql = "delete from {table} where {产品名称}='{名称}';".format(table=self.table, 名称=key, 产品名称=self.cols[1])
        elif func == "2":
            sql = "insert into {table} ({col0}, {col1}, {col2}, {col3}, {col4}) " \
                  "values('{产品名称}','{产品编号}','{产品金额}','{库存数量}','{数量范围}');".format(table=self.table,
                                                                                 产品名称=key[0], 产品编号=key[1], 产品金额=key[2],
                                                                                 库存数量=key[3], 数量范围=key[4],
                                                                                 col0=self.cols[1], col1=self.cols[2],
                                                                                 col2=self.cols[3], col3=self.cols[4],
                                                                                 col4=self.cols[5]
                                                                                 )
        elif func == "3":
            sql = "update {table} set {列名}='{值}' where 产品名称='{名称}'".format(table=self.table, 列名=key[0], 值=key[1],
                                                                           名称=key[2])
        elif func == "4":
            sql = '''select 产品名称, 库存数量, 数量范围 from {table}'''.format(table=self.table)
        elif func == "5":
            sql = '''select {col_name} from {table}'''.format(col_name=key, table=self.table)
        else:
            sql = None
        if self._check_sql(sql):
            return sql
        print('''Please enter the function you want to use: 
                0: get all data from database,
                1: delete one specific line in database,
                2: add a new line in database,
                3: update a value in database,
                4: update the rest space of products
                5. search the specific col''')

    def checkrest(self):
        res_names = []
        connect = sqlite3.connect(self.db_dir)
        c = connect.cursor()
        checkrest_sql = self._sql_gen(func="4")
        rests = [rest for rest in c.execute(checkrest_sql)]
        for rest in rests:
            name, remain = rest[0], int(rest[2].split(",")[1]) - rest[1]
            if remain > 0:
                res_names.append(name)
                c.execute(self._sql_gen("3", key=["剩余容量", remain, name]))
            else:
                c.execute(self._sql_gen("3", key=["剩余容量", 0, name]))
        data_sql = self._sql_gen("0")
        if self._check_sql(data_sql):
            self.data = [list(row) for row in c.execute(data_sql)]
        connect.commit()
        c.close()
        connect.close()
        print("The rest capacity of database has been updated!")
        return res_names

    def delete(self, keys=None):
        connect = sqlite3.connect(self.db_dir)
        c = connect.cursor()
        delete_sql = self._sql_gen("1", key=keys)
        c.execute(delete_sql)
        data_sql = self._sql_gen("0")
        if self._check_sql(data_sql):
            self.data = [list(row) for row in c.execute(data_sql)]
        connect.commit()
        c.close()
        connect.close()
        print("{} has been deleted".format(keys))

    def update(self, keys):
        connect = sqlite3.connect(self.db_dir)
        c = connect.cursor()
        update_sql = self._sql_gen("3", key=keys)
        c.execute(update_sql)
        data_sql = self._sql_gen("0")
        if self._check_sql(data_sql):
            self.data = [list(row) for row in c.execute(data_sql)]
        connect.commit()
        c.close()
        connect.close()
        print("{} has been updated".format(" ".join(map(str, keys))))

    def insert(self, keys):
        connect = sqlite3.connect(self.db_dir)
        c = connect.cursor()
        insert_sql = self._sql_gen("2", key=keys)
        c.execute(insert_sql)
        data_sql = self._sql_gen("0")
        if self._check_sql(data_sql):
            self.data = [list(row) for row in c.execute(data_sql)]
        connect.commit()
        c.close()
        connect.close()
        print("{} has been inserted".format(" ".join(map(str, keys))))


if __name__ == '__main__':
    '''
        This is the example for database loading, data inserting, deleting, updating, and row info illustrating...
    '''
    db = Database()
    db.loading("库存.db")
    # db.insert(["test", "111", 2, 4, "2,9"])
    db.info()
    # db.delete('test')
    db.update(["库存数量", 4, "螺旋藻片"])
    db.info()
    # db.update(["库存数量", 1, "螺旋藻片"])
    # db.row_info(keys=["芦荟胶", "水润面膜"])
