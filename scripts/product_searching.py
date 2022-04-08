import random


class Fproduct():
    def __init__(self, data, money, special_case=False):
        self.all_choices = []
        self.standard_money = 4000
        self.data = data
        self.aim_money = money
        self.special_case = special_case
        self.record_base = [{}, 0]
        self.prefer = []  # 优先选择的物品
        self.final_choices = []

    def _check_data(self):
        return bool(self.data)

    def _fill(self):
        if self._check_data():
            for items in self.data:
                least = int(items[5].split(",")[0])
                fill_money = (least - items[4]) * items[3]
                if fill_money > 0 and self.aim_money >= fill_money + self.standard_money:
                    self.aim_money -= fill_money
                    self.record_base[0][items[1]] = self.record_base[0].get(items[1], 0) + (least - items[4])
        else:
            self.special_case = True

    def _overflow(self, counter, product):
        try:
            for row in self.data:
                if product in row:
                    if counter[product] < row[6]:
                        return False
            return True
        except KeyError:
            return False

    def _duplicate(self, temp_res):
        if not self.all_choices or not temp_res:
            return False
        for old_res in self.all_choices:
            if temp_res == old_res:
                return True
        return False

    def _random_gen(self):
        num_list = []
        for _ in range(20):
            num = random.randint(0, len(self.all_choices))
            if num not in num_list:
                num_list.append(num)
                self.final_choices.append(self.all_choices[num])

    def matching(self):
        '''
        1. 找出所有未达到最大值的物品，如果小于最小值直接添加到最小值并扣除指定钱数（并记录可容纳的个数）
        2. 使用筛选出的物品进行BFS算法
            a. 等于指定金额
                1) 是否存在相同组合 -> 否，保存；
            b. 大于指定金额 -> 退出递归
            c. 小于指定金额 （可进一步优化）
                1) 选择当前物品是否超出数量范围 -> 否，继续搜索；是，continue
        :return:
        '''
        self._fill()
        self._planA(result=self.record_base)
        self._random_gen()
        return self.final_choices, self.data

    def _planA(self, result=None):
        if result[1] == self.aim_money and not self._duplicate(result[0]):
            self.all_choices.append(result[0])
            return
        elif result[1] > self.aim_money:
            return
        else:
            for item in self.data:
                if len(self.all_choices) == 300:
                    break
                temp_counter = result[0].copy()
                if not self._overflow(result[0], item[1]):
                    temp_counter[item[1]] = 1 + temp_counter.get(item[1], 0)
                    temp_money = result[1] + item[3]
                    self._planA([temp_counter, temp_money])
                    temp_counter = result[0].copy()
                    temp_money = result[1]
            return


if __name__ == '__main__':
    # money = 600
    # data = [['1', 190, 25, '18,34'], ['2', 340, 15, '7,23'], ['3', 150, 11, '10,21'], ['4', 390, 33, '8,24'],
    #         ['5', 170, 30, '6,25'], ['6', 210, 5, '17,21'], ['7', 160, 32, '19,32'], ['8', 210, 6, '19,29'],
    #         ['9', 340, 9, '11,33'], ['10', 400, 23, '12,32']]
    # Fproduct(data, money).matching()
    dict1 = {"1": 2, "3": 4, "2": 3, "4": 5}
    dict2 = {"1": 2, "2": 3, "3": 4, "4": 5}
    print(id(dict1))
    print(id(dict2))
    print(dict1 == dict2)