from collections import deque
import numpy as np
import random


class loa_env():
    def __init__(self):
        self.board_weight = [0.3, 0.5, 0.2]
        self.card_weight = [0.95,0.05]
        #self.board = np.random.choice([0,1,2], size=(9,9), p = self.board_weight)
        self.board = [[0]*9 for _ in range(9)]

        self.hand = {0 : 0, 1 : 0}  # 0 : left, 1 : right
        self.deck = deque()     # (card : 1~12, grade : 1~3)
        nrow, ncol = 9, 9
        self.nA = 164     # 0~161 : 9*9 left use & right use, 162 : left reroll, 163 : right reroll
        self.nS = nrow * ncol + 5   # 9*9 board + 2 hand + 3 deck = 86
        self.card_list = ['none', 'uphwa', 'daepokbal' 'byeolag', 'nakreah', 'yongoreom', 'bunchul',
             'pokpongu', 'haeil', 'chonggeokpa', 'jijin', 'jeonghwa', 'gongmeong']
        self.observation_space = nrow * ncol + 5 + 5
        self.action_space = 164


    def step(self, action):
        
        if action < 162:
            lr = action % 2     # lr == 0 : left, lr == 1 : right
            aa = action // 2
            arow, acol = aa // 9, aa % 9
            h_card, h_grade = self.hand[lr]
            tmp = self.deck.popleft()
            self.deck.append((np.random.randint(1,13), np.random.choice([1,2], p = self.card_weight)))
            self.hand[lr] = tmp

            self.board[arow][acol] = 0
            if h_card == 1:     # 업화
                rc_list = [(-2,0),(-1,-1),(-1,0),(-1,1),(0,-2),(0,-1),(0,1),(0,2),(1,-1),(1,0),(1,1),(2,0)]
                if h_grade == 1:    # 1단계
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 1:
                            if np.random.rand() < 0.5:
                                self.board[nr][nc] = 0
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 2:
                            zero_list = []
                            if np.random.rand() < 0.5:
                                for i in range(9):
                                    for j in range(9):
                                        if self.board[i][j] == 0:
                                            zero_list.append((i,j))
                                if len(zero_list) < 3:
                                    for i,j in zero_list:
                                        self.board[i][j] = 1
                                else:
                                    for i,j in random.sample(zero_list, 3):
                                        self.board[i][j] = 1
                if h_grade == 2:
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 1:
                            self.board[nr][nc] = 0

                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 2:
                            zero_list = []
                            for i in range(9):
                                for j in range(9):
                                    if self.board[i][j] == 0:
                                        zero_list.append((i,j))
                            if len(zero_list) < 3:
                                for i,j in zero_list:
                                    self.board[i][j] = 1
                            else:
                                for i,j in random.sample(zero_list, 3):
                                    self.board[i][j] = 1
                if h_grade == 3:
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0 or self.board[nr][nc] == 2:
                            continue
                        if self.board[nr][nc] == 1:
                            self.board[nr][nc] = 0                 
            if h_card == 2:     # 대폭발
                rc_list = [(-1,-1),(-1,1),(1,-1),(1,1)]

                if h_grade == 1:
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        percent = 1
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            percent -= 0.15
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 1:
                                if np.random.rand() < percent:
                                    self.board[nr][nc] = 0
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        percent = 1
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            percent -= 0.15
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 2:
                                zero_list = []
                                if np.random.rand() < percent:
                                    for i in range(9):
                                        for j in range(9):
                                            if self.board[i][j] == 0:
                                                zero_list.append((i,j))
                                    if len(zero_list) < 3:
                                        for i,j in zero_list:
                                            self.board[i][j] = 1
                                    else:
                                        for i,j in random.sample(zero_list, 3):
                                            self.board[i][j] = 1
                if h_grade == 2:
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 1:
                                    self.board[nr][nc] = 0
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 2:
                                    zero_list = []
                                    for i in range(9):
                                        for j in range(9):
                                            if self.board[i][j] == 0:
                                                zero_list.append((i,j))
                                    if len(zero_list) < 3:
                                        for i,j in zero_list:
                                            self.board[i][j] = 1
                                    else:
                                        for i,j in random.sample(zero_list, 3):
                                            self.board[i][j] = 1
                if h_grade == 3:
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 1:
                                    self.board[nr][nc] = 0
            if h_card == 3:     # 벼락
                one_list = []
                zero_list = []
                for i in range(9):
                    for j in range(9):
                        if self.board[i][j] == 1:
                            one_list.append((i,j))
                if h_grade == 1:        # 확률 몰라서 걍 uniform
                    delete_num = np.random.randint(0,3)
                if h_grade == 2:
                    delete_num = np.random.randint(0,5)
                if h_grade == 3:
                    delete_num = np.random.randint(0,7)
                if len(one_list) < delete_num:
                    for i,j in one_list:
                        self.board[i][j] = 0
                else:
                    for i,j in random.sample(one_list, delete_num):
                        self.board[i][j] = 0

                for i in range(9):
                    for j in range(9):
                        if self.board[i][j] == 0:
                            zero_list.append((i,j))
                if np.random.rand() < 0.25: # 확률 몰라서 걍 0.25
                    for i,j in random.sample(zero_list,1):
                        self.board[i][j] = 1
            if h_card == 4:     # 낙뢰
                rc_list = [(-1,0),(0,-1),(0,1),(1,0)]
                if h_grade == 1:    # 1단계
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 1:
                            if np.random.rand() < 0.5:
                                self.board[nr][nc] = 0
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 2:
                            zero_list = []
                            if np.random.rand() < 0.5:
                                for i in range(9):
                                    for j in range(9):
                                        if self.board[i][j] == 0:
                                            zero_list.append((i,j))
                                if len(zero_list) < 3:
                                    for i,j in zero_list:
                                        self.board[i][j] = 1
                                else:
                                    for i,j in random.sample(zero_list, 3):
                                        self.board[i][j] = 1
                if h_grade == 2:
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 1:
                            self.board[nr][nc] = 0

                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 2:
                            zero_list = []
                            for i in range(9):
                                for j in range(9):
                                    if self.board[i][j] == 0:
                                        zero_list.append((i,j))
                            if len(zero_list) < 3:
                                for i,j in zero_list:
                                    self.board[i][j] = 1
                            else:
                                for i,j in random.sample(zero_list, 3):
                                    self.board[i][j] = 1
                if h_grade == 3:
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0 or self.board[nr][nc] == 2:
                            continue
                        if self.board[nr][nc] == 1:
                            self.board[nr][nc] = 0
            if h_card == 5:     # 용오름
                rc_list = [(-1,-1),(-1,1),(1,1),(1,-1)]
                if h_grade == 1:    # 1단계
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 1:
                            if np.random.rand() < 0.5:
                                self.board[nr][nc] = 0
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 2:
                            zero_list = []
                            if np.random.rand() < 0.5:
                                for i in range(9):
                                    for j in range(9):
                                        if self.board[i][j] == 0:
                                            zero_list.append((i,j))
                                if len(zero_list) < 3:
                                    for i,j in zero_list:
                                        self.board[i][j] = 1
                                else:
                                    for i,j in random.sample(zero_list, 3):
                                        self.board[i][j] = 1
                if h_grade == 2:
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 1:
                            self.board[nr][nc] = 0

                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 2:
                            zero_list = []
                            for i in range(9):
                                for j in range(9):
                                    if self.board[i][j] == 0:
                                        zero_list.append((i,j))
                            if len(zero_list) < 3:
                                for i,j in zero_list:
                                    self.board[i][j] = 1
                            else:
                                for i,j in random.sample(zero_list, 3):
                                    self.board[i][j] = 1
                if h_grade == 3:
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0 or self.board[nr][nc] == 2:
                            continue
                        if self.board[nr][nc] == 1:
                            self.board[nr][nc] = 0
            #if h_card == 6:      분출 pass
            if h_card == 7:     # 폭풍우
                rc_list = [(1,0),(-1,0)]
                if h_grade == 1:
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        percent = 1
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            percent -= 0.15
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 1:
                                if np.random.rand() < percent:
                                    self.board[nr][nc] = 0
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        percent = 1
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            percent -= 0.15
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 2:
                                zero_list = []
                                if np.random.rand() < percent:
                                    for i in range(9):
                                        for j in range(9):
                                            if self.board[i][j] == 0:
                                                zero_list.append((i,j))
                                    if len(zero_list) < 3:
                                        for i,j in zero_list:
                                            self.board[i][j] = 1
                                    else:
                                        for i,j in random.sample(zero_list, 3):
                                            self.board[i][j] = 1
                if h_grade == 2:
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 1:
                                    self.board[nr][nc] = 0
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 2:
                                    zero_list = []
                                    for i in range(9):
                                        for j in range(9):
                                            if self.board[i][j] == 0:
                                                zero_list.append((i,j))
                                    if len(zero_list) < 3:
                                        for i,j in zero_list:
                                            self.board[i][j] = 1
                                    else:
                                        for i,j in random.sample(zero_list, 3):
                                            self.board[i][j] = 1
                if h_grade == 3:
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 1:
                                    self.board[nr][nc] = 0
            if h_card == 8:     # 해일
                rc_list = [(1,0),(-1,0),(0,1),(0,-1)]
                if h_grade == 1:
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        percent = 1
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            percent -= 0.15
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 1:
                                if np.random.rand() < percent:
                                    self.board[nr][nc] = 0
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        percent = 1
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            percent -= 0.15
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 2:
                                zero_list = []
                                if np.random.rand() < percent:
                                    for i in range(9):
                                        for j in range(9):
                                            if self.board[i][j] == 0:
                                                zero_list.append((i,j))
                                    if len(zero_list) < 3:
                                        for i,j in zero_list:
                                            self.board[i][j] = 1
                                    else:
                                        for i,j in random.sample(zero_list, 3):
                                            self.board[i][j] = 1
                if h_grade == 2:
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 1:
                                    self.board[nr][nc] = 0
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 2:
                                    zero_list = []
                                    for i in range(9):
                                        for j in range(9):
                                            if self.board[i][j] == 0:
                                                zero_list.append((i,j))
                                    if len(zero_list) < 3:
                                        for i,j in zero_list:
                                            self.board[i][j] = 1
                                    else:
                                        for i,j in random.sample(zero_list, 3):
                                            self.board[i][j] = 1
                if h_grade == 3:
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 1:
                                    self.board[nr][nc] = 0
            if h_card == 9:     # 충격파
                rc_list = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
                if h_grade == 1:    # 1단계
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 1:
                            if np.random.rand() < 0.75:
                                self.board[nr][nc] = 0
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 2:
                            zero_list = []
                            if np.random.rand() < 0.75:
                                for i in range(9):
                                    for j in range(9):
                                        if self.board[i][j] == 0:
                                            zero_list.append((i,j))
                                if len(zero_list) < 3:
                                    for i,j in zero_list:
                                        self.board[i][j] = 1
                                else:
                                    for i,j in random.sample(zero_list, 3):
                                        self.board[i][j] = 1
                if h_grade == 2:
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 1:
                            self.board[nr][nc] = 0

                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 2:
                            zero_list = []
                            for i in range(9):
                                for j in range(9):
                                    if self.board[i][j] == 0:
                                        zero_list.append((i,j))
                            if len(zero_list) < 3:
                                for i,j in zero_list:
                                    self.board[i][j] = 1
                            else:
                                for i,j in random.sample(zero_list, 3):
                                    self.board[i][j] = 1
                if h_grade == 3:
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0 or self.board[nr][nc] == 2:
                            continue
                        if self.board[nr][nc] == 1:
                            self.board[nr][nc] = 0
            if h_card == 10:    # 지진
                rc_list = [(0,1),(0,-1)]
                if h_grade == 1:
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        percent = 1
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            percent -= 0.15
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 1:
                                if np.random.rand() < percent:
                                    self.board[nr][nc] = 0
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        percent = 1
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            percent -= 0.15
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 2:
                                zero_list = []
                                if np.random.rand() < percent:
                                    for i in range(9):
                                        for j in range(9):
                                            if self.board[i][j] == 0:
                                                zero_list.append((i,j))
                                    if len(zero_list) < 3:
                                        for i,j in zero_list:
                                            self.board[i][j] = 1
                                    else:
                                        for i,j in random.sample(zero_list, 3):
                                            self.board[i][j] = 1
                if h_grade == 2:
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 1:
                                    self.board[nr][nc] = 0
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 2:
                                    zero_list = []
                                    for i in range(9):
                                        for j in range(9):
                                            if self.board[i][j] == 0:
                                                zero_list.append((i,j))
                                    if len(zero_list) < 3:
                                        for i,j in zero_list:
                                            self.board[i][j] = 1
                                    else:
                                        for i,j in random.sample(zero_list, 3):
                                            self.board[i][j] = 1
                if h_grade == 3:
                    for r,c in rc_list:
                        nr, nc = arow, acol
                        for _ in range(8):
                            nr,nc = nr+r,nc+c
                            if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                                break
                            if self.board[nr][nc] == 1:
                                    self.board[nr][nc] = 0
            if h_card == 11:    # 정화
                rc_list = [(0,-1),(0,1)]
                if h_grade == 1:    # 1단계
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 1 or self.board[nr][nc] == 2:
                            if np.random.rand() < 0.5:
                                self.board[nr][nc] = 0
                if h_grade == 2:
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 1 or self.board[nr][nc] == 2:
                            self.board[nr][nc] = 0
                if h_grade == 3:
                    rc_list = [(0,-1),(0,1),(1,0),(-1,0)]
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0 :
                            continue
                        if self.board[nr][nc] == 1 or self.board[nr][nc] == 2:
                            self.board[nr][nc] = 0
            if h_card == 12:    # 공명
                rc_list = [(0,-1),(0,-2),(0,1),(0,2),(1,0),(2,0),(-1,0),(-2,0)]
                if h_grade == 1:    # 1단계
                    for r, c in rc_list:
                        nr, nc = arow+r, acol+c
                        if nr < 0 or nr >= 9 or nc < 0 or nc >= 9:
                            continue
                        if self.board[nr][nc] == 0:
                            continue
                        if self.board[nr][nc] == 1 or self.board[nr][nc] == 2:
                            self.board[nr][nc] = 0

        else:       # reroll
            tmp = self.deck.popleft()
            self.deck.append((np.random.randint(1,13), np.random.choice([1,2], p = self.card_weight)))
            if action == 162:
                self.hand[0] = tmp
            if action == 163:
                self.hand[1] = tmp
            reward = 0
            is_done = False
        
        state = []
        for i in range(9):
            for j in range(9):
                state.append(self.board[i][j])
        state.append(self.hand[0][0])
        state.append(self.hand[0][1])
        state.append(self.hand[1][0])
        state.append(self.hand[1][1])
        for _ in range(3):
            tmp = self.deck.popleft()
            state.append(tmp[0])
            state.append(tmp[1])
            self.deck.append(tmp)

        cnt = 0
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 1:
                    cnt += 1
        if cnt == 0:
            reward = 100
            is_done = True
        else:
            reward = -cnt
            is_done = False
        return state, reward, is_done
    
    def reset(self):

        self.board = np.random.choice([0,1,2], size=(9,9), p = self.board_weight)

        for _ in range(3):
            self.deck.append((np.random.randint(1,13), np.random.choice([1,2], p = self.card_weight)))
        self.hand[0] = (np.random.randint(1,13), np.random.choice([1,2], p = self.card_weight))
        self.hand[1] = (np.random.randint(1,13), np.random.choice([1,2], p = self.card_weight))
        state = []
        for i in range(9):
            for j in range(9):
                state.append(self.board[i][j])
        state.append(self.hand[0][0])
        state.append(self.hand[0][1])
        state.append(self.hand[1][0])
        state.append(self.hand[1][1])
        for _ in range(3):
            tmp = self.deck.popleft()
            state.append(tmp[0])
            state.append(tmp[1])
            self.deck.append(tmp)
        # reward = 0
        # done = False
        return state #, reward, done
