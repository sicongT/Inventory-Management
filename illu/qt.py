from PySide2.QtCore import QFile, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QTableWidgetItem, QMessageBox
from utils import database
from scripts import product_searching


class MyUI():
    def __init__(self, ui_file):
        super().__init__()
        self.current_data = None
        self.headers = None
        self.types = [int, int, str]
        self.has_loaded = False
        # 从文件中加载UI定义
        qfile = QFile(ui_file)
        qfile.open(QFile.ReadOnly)
        qfile.close()

        # 从UI定义中动态创建一个相应的窗口对象
        self.ui = QUiLoader().load(qfile)
        # 初始化金额
        self.money = self.ui.money_input
        # 初始化数据库表
        self.table = self.ui.data_table
        # 初始化列表
        self.combo_list = self.ui.listWidget
        # 加载产品名称
        self.ui.product_list.addItems(self.name_list())
        # 点击“加载”响应
        self.ui.search_button.clicked.connect(self.load)
        # 点击“提交”响应  目前空闲中，可作用于其他功能
        # self.ui.push_button.clicked.connect(self.update)

        # 如果加载完毕，修改产品数据的响应
        self.table.cellChanged.connect(self.change)
        # 点击“开始”响应
        self.ui.start_button.clicked.connect(self.money_check)
        # 点击"选择"相应
        self.ui.choose_button.clicked.connect(self.update)
        self.ui.show()
    # def combo_selection(self):

    def combo_show(self, comboes):
        show_list = []
        for combo in comboes:
            res = []
            for key, val in combo.items():
                product = key + " " + str(val)
                res.append(product)
            choice = ",".join(res)
            show_list.append(choice)
        self.combo_list.addItems(show_list)

    def combo(self, money):
        data = database.Database()
        data.loading()
        name = data.checkrest()
        IS_SPECIAL = False
        if name:
            available = data.row_info(name)
        else:
            available = data.get_data()
            IS_SPECIAL = True
        find_func = product_searching.Fproduct(available, money, IS_SPECIAL)
        choices, new_data = find_func.matching()
        return choices

    def money_check(self):
        try:
            money = int(self.money.text())
            if money > 50000:
                choice = QMessageBox.question(
                    self.ui,
                    "确认",
                    "请确认输入金额:{} 是否正确！".format(money)
                )
                if choice == QMessageBox.Yes:
                    choices = self.combo(money=money)
                    self.combo_show(choices)
                if choice == QMessageBox.No:
                    self.money.clear()
            elif money < 0:
                raise ValueError
            else:
                choices = self.combo(money=money)
                self.combo_show(choices)
        except ValueError:
            QMessageBox.warning(
                self.ui,
                '输入内容不正确',
                '请输入一个数字！')
            self.money.clear()
#######################################################################################################################
    def change(self, row, col):
        if self.has_loaded:
            try:
                content = self.types[col - 2](self.table.item(row, col).text())
                if col==4:
                    assert int(content.split(",")[0]) and int(content.split(",")[1])
                    assert int(content.split(",")[0]) < int(content.split(",")[1])
                name = self.table.item(row, 0).text()
                choice = QMessageBox.question(
                    self.ui,
                    '提示',
                    '确定要将"{}"的{}修改为{}吗？'.format(name, self.headers[col+1], content))
                if choice == QMessageBox.Yes:
                    for row in self.current_data:
                        if name in row:
                            row[col + 1] = content
                    self.update()
                if choice == QMessageBox.No:
                    self.load()
            except Exception:
                QMessageBox.critical(
                    self.ui,
                    '错误',
                    '请输入正确的内容！')
                self.load()

    def update(self):
        try:
            "update {table} set {列名}='{值}' where 产品名称='{名称}'"
            db = database.Database()
            for product in self.current_data:
                for i in range(3, len(product) -1):
                    db.update(keys=[self.headers[i], product[i], product[1]])
            self.load()
        except Exception:
            QMessageBox.critical(
                self.ui,
                '错误',
                '请先进行查询步骤！')

    def name_list(self):
        db = database.Database()
        db.loading()
        lst = ["-"]
        rows = db.get_data()
        for row in rows:
            lst.append(row[1])
        return lst

    def load(self):
        # 选中产品相应
        self.has_loaded = False
        product = self.ui.product_list.currentText()
        # 加载数据库
        db = database.Database()
        db.loading()
        self.current_data = db.get_data()
        if product == "-":
            rows = self.current_data
        else:
            rows = db.row_info(keys=[product])
        row = len(rows)
        col = len(rows[0])
        self.headers = db.get_header_name()

        # 设置表格大小
        self.table.setRowCount(row)
        self.table.setColumnCount(len(self.headers) - 2)

        # 设置列表头
        for i in range(len(self.headers) - 2):
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(self.headers[i+1]))

        # 插入数据
        for i in range(row):
            for j in range(1, col - 1):
                item = QTableWidgetItem(str(rows[i][j]))
                if j == 1 or j == 2:
                    item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignHCenter)
                self.table.setItem(i, j-1, item)
        self.has_loaded = True
