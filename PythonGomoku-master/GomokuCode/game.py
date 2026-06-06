import os
import time

AI_USE_CPP = False

if not AI_USE_CPP:  # 是否用C++版的AI脚本
    from ai import AI1Step
else:
    import example


class Gomoku:

    def __init__(self, human_first=True):
        """
        初始化五子棋游戏
        :param human_first: True表示人类玩家先手，False表示电脑先手
        """
        self.g_map = [[0 for y in range(15)] for x in range(15)]  # 当前的棋盘
        self.cur_step = 0  # 步数
        self.max_search_steps = 3  # 最远搜索2回合之后
        self.human_first = human_first  # 记录谁先手，True为人类先手，False为电脑先手

    def move_1step(self, input_by_window=False, pos_x=None, pos_y=None):
        """
        玩家落子
        :param input_by_window: 是否从图形界面输入
        :param pos_x: 从图形界面输入时，输入的x坐标为多少
        :param pos_y: 从图形界面输入时，输入的y坐标为多少
        """
        while True:
            try:
                if not input_by_window:
                    pos_x = int(input('x: '))  # 接受玩家的输入人
                    pos_y = int(input('y: '))
                if 0 <= pos_x <= 14 and 0 <= pos_y <= 14:  # 判断这个格子能否落子
                    if self.g_map[pos_x][pos_y] == 0:
                        self.g_map[pos_x][pos_y] = 1
                        self.cur_step += 1
                        return
            except ValueError:  # 玩家输入不正确的情况（例如输入了‘A’）
                continue

    def game_result(self, show=False):
        """判断游戏的结局。0为游戏进行中，1为玩家获胜，2为电脑获胜，3为平局"""
        # 1. 判断是否横向连续五子
        for x in range(11):
            for y in range(15):
                if self.g_map[x][y] == 1 and self.g_map[x + 1][y] == 1 and self.g_map[x + 2][y] == 1 and self.g_map[x + 3][y] == 1 and self.g_map[x + 4][y] == 1:
                    if show:
                        return 1, [(x0, y) for x0 in range(x, x + 5)]
                    else:
                        return 1
                if self.g_map[x][y] == 2 and self.g_map[x + 1][y] == 2 and self.g_map[x + 2][y] == 2 and self.g_map[x + 3][y] == 2 and self.g_map[x + 4][y] == 2:
                    if show:
                        return 2, [(x0, y) for x0 in range(x, x + 5)]
                    else:
                        return 2

        # 2. 判断是否纵向连续五子
        for x in range(15):
            for y in range(11):
                if self.g_map[x][y] == 1 and self.g_map[x][y + 1] == 1 and self.g_map[x][y + 2] == 1 and self.g_map[x][y + 3] == 1 and self.g_map[x][y + 4] == 1:
                    if show:
                        return 1, [(x, y0) for y0 in range(y, y + 5)]
                    else:
                        return 1
                if self.g_map[x][y] == 2 and self.g_map[x][y + 1] == 2 and self.g_map[x][y + 2] == 2 and self.g_map[x][y + 3] == 2 and self.g_map[x][y + 4] == 2:
                    if show:
                        return 2, [(x, y0) for y0 in range(y, y + 5)]
                    else:
                        return 2

        # 3. 判断是否有左上-右下的连续五子
        for x in range(11):
            for y in range(11):
                if self.g_map[x][y] == 1 and self.g_map[x + 1][y + 1] == 1 and self.g_map[x + 2][y + 2] == 1 and self.g_map[x + 3][y + 3] == 1 and self.g_map[x + 4][y + 4] == 1:
                    if show:
                        return 1, [(x + t, y + t) for t in range(5)]
                    else:
                        return 1
                if self.g_map[x][y] == 2 and self.g_map[x + 1][y + 1] == 2 and self.g_map[x + 2][y + 2] == 2 and self.g_map[x + 3][y + 3] == 2 and self.g_map[x + 4][y + 4] == 2:
                    if show:
                        return 2, [(x + t, y + t) for t in range(5)]
                    else:
                        return 2

        # 4. 判断是否有右上-左下的连续五子
        for x in range(11):
            for y in range(11):
                if self.g_map[x + 4][y] == 1 and self.g_map[x + 3][y + 1] == 1 and self.g_map[x + 2][y + 2] == 1 and self.g_map[x + 1][y + 3] == 1 and self.g_map[x][y + 4] == 1:
                    if show:
                        return 1, [(x + t, y + 4 - t) for t in range(5)]
                    else:
                        return 1
                if self.g_map[x + 4][y] == 2 and self.g_map[x + 3][y + 1] == 2 and self.g_map[x + 2][y + 2] == 2 and self.g_map[x + 1][y + 3] == 2 and self.g_map[x][y + 4] == 2:
                    if show:
                        return 2, [(x + t, y + 4 - t) for t in range(5)]
                    else:
                        return 2

        # 5. 判断是否为平局
        for x in range(15):
            for y in range(15):
                if self.g_map[x][y] == 0:  # 棋盘中还有剩余的格子，不能判断为平局
                    if show:
                        return 0, [(-1, -1)]
                    else:
                        return 0

        if show:
            return 3, [(-1, -1)]
        else:
            return 3

    def ai_move_1step(self):
        """电脑落子（简单版，按顺序找第一个空位）"""
        for x in range(15):
            for y in range(15):
                if self.g_map[x][y] == 0:
                    self.g_map[x][y] = 2
                    self.cur_step += 1
                    return
                
    def ai_move_indicated_1step(self, x=7, y=7):
        self.g_map[7][7] = 2
        # self.cur_step += 1
        return

    def ai_play_1step_by_cpp(self):
        # ai = AI1Step(self, self.cur_step, True)  # AI判断下一步执行什么操作
        st = time.time()
        mapstring = list()
        for x in range(15):
            mapstring.extend(self.g_map[x])
        try:
            node_len, ai_ope_x, ai_poe_y = example.ai_1step(self.cur_step, int(True), self.max_search_steps, mapstring)
            ai_ope = [ai_ope_x, ai_poe_y]
        except ValueError:
            raise ValueError('AI程序计算出来的数值不正确')
        ed = time.time()
        print('生成了%d个节点，用时%.4f' % (node_len, ed - st))
        self.g_map[ai_ope[0]][ai_ope[1]] = 2
        self.cur_step += 1

    def ai_play_1step_py_python(self):
        ai = AI1Step(self, self.cur_step, True)  # AI判断下一步执行什么操作
        st = time.time()
        ai.search(0, [set(), set()], self.max_search_steps)  # 最远看2回合之后
        ed = time.time()
        print('生成了%d个节点，用时%.4f，评价用时%.4f' % (len(ai.method_tree), ed - st, ai.t))
        if ai.next_node_dx_list[0] == -1:
                raise ValueError('ai.next_node_dx_list[0] == -1')
        ai_ope = ai.method_tree[ai.next_node_dx_list[0]].ope
        if self.g_map[ai_ope[0]][ai_ope[1]] != 0:
            raise ValueError('self.game_map[ai_ope[0]][ai_ope[1]] = %d' % self.g_map[ai_ope[0]][ai_ope[1]])
        self.g_map[ai_ope[0]][ai_ope[1]] = 2
        self.cur_step += 1

    def ai_play_1step(self):
        if AI_USE_CPP:
            self.max_search_steps = 3
            self.ai_play_1step_by_cpp()
        else:
            self.max_search_steps = 2
            self.ai_play_1step_py_python()

    def show(self, res):
        """显示游戏内容"""
        for y in range(15):
            for x in range(15):
                if self.g_map[x][y] == 0:
                    print('  ', end='')
                elif self.g_map[x][y] == 1:
                    print('〇', end='')
                elif self.g_map[x][y] == 2:
                    print('×', end='')

                if x != 14:
                    print('-', end='')
            print('\n', end='')
            for x in range(15):
                print('|  ', end='')
            print('\n', end='')

        if res == 1:
            print('玩家获胜!')
        elif res == 2:
            print('电脑获胜!')
        elif res == 3:
            print('平局!')

    def play(self):
        """
        游戏主循环，根据human_first标记分两套流程执行
        人类先手流程：玩家 -> AI -> 玩家 -> AI ...
        电脑先手流程：AI -> 玩家 -> AI -> 玩家 ...
        """
        if self.human_first:
            # 人类先手流程
            while True:
                # 玩家落子
                self.move_1step()
                res = self.game_result()
                if res != 0:
                    self.show(res)
                    return
                
                # AI落子
                self.ai_play_1step()
                res = self.game_result()
                if res != 0:
                    self.show(res)
                    return
                
                self.show(0)  # 显示当前棋盘状态
        else:
            print(self.human_first)
            # 电脑先手流程
            while True:
                # AI先落子
                self.ai_play_1step()
                res = self.game_result()
                if res != 0:
                    self.show(res)
                    return
                
                self.show(0)  # 显示AI落子后的棋盘
                
                # 玩家落子
                self.move_1step()
                res = self.game_result()
                if res != 0:
                    self.show(res)
                    return
                
                self.show(0)  # 显示玩家落子后的棋盘

    def map2string(self):
        mapstring = list()
        for x in range(15):
            mapstring.extend(list(map(lambda x0: x0 + 48, self.g_map[x])))
        return bytearray(mapstring).decode('utf8')