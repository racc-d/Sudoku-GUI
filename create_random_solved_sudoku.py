#Trying to build a sudoku grid generator
import random
from itertools import chain

def generate_sudoku():
    while True:
        try:
            grid = []
            for i in range(9):
                grid.append([])
                for j in range(9):
                    grid[i].append(0)
            grid[0] = random.sample(list(range(1, 10)), 9)
            for i in range(1, 9):
                for j in range(9):
                    col_filled = [grid[m][j] for m in range(9) if grid[m][j] != 0]
                    # print(col_filled)
                    h, k = i//3, j//3
                    box_filled = [grid[(h*3)+i][(k*3): (k*3)+3] for i in range(3)]
                    box_filled = list(chain.from_iterable(box_filled))
                    box_filled = [i for i in box_filled if i !=0]
                    filled = list(set(col_filled) | set(box_filled))
                    register = [m for m in grid[i] if m !=0]
                    filled = list(set(filled) | set(register))
                    g = filled[:]
                    options = [1,2,3,4,5,6,7,8,9]
                    for s in g:
                        options.remove(s)
                    grid[i][j] = random.choice(options)
            break
        except IndexError:
            pass



    def valid():

        #Checking Rows for duplicates

        for i in range(len(grid)):
            for j in grid[i]:
                if grid[i].count(j) > 1:
                    return False


            col = []
            for h in range(len(grid[i])):
                col.append(grid[h][i])

            #Checking columns for duplicates

            for i in col:
                if col.count(i) > 1:
                    return False

        #Checking boxes for duplicates

        box_1 = grid[0][:3] + grid[1][:3] + grid[2][:3]
        box_2 = grid[0][3:6] + grid[1][3:6] + grid[2][3:6]
        box_3 = grid[0][6:9] + grid[1][6:9] + grid[2][6:9]

        box_4 = grid[3][:3] + grid[4][:3] + grid[5][:3]
        box_5 = grid[3][3:6] + grid[4][3:6] + grid[5][3:6]
        box_6 = grid[3][6:9] + grid[4][6:9] + grid[5][6:9]

        box_7 = grid[6][:3] + grid[7][:3] + grid[8][:3]
        box_8 = grid[6][3:6] + grid[7][3:6] + grid[8][3:6]
        box_9 = grid[6][6:9] + grid[7][6:9] + grid[8][6:9]

        for i in range(1, 10):
            for j in eval('box_%d' % i):
                if list(eval('box_%d' % i)).count(j) > 1:
                    return False

        return True

    while True:
        if valid():
            break

    return grid
