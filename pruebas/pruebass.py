#!/usr/bin/python
import sys


class Cell(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return "(" + str(self.row) + "," + str(self.col) + ")"


class Rule(object):
    def __init__(self, value, cells):
        self.cells = cells
        self.value = value

    def __str__(self):
        retStr = "value=" + str(self.value) + " cells=[ "
        for cell in self.cells:
            retStr += str(cell) + " "
        retStr += "]"
        return retStr


def is_solution(board, rules):
    for rule in rules:
        current_value = 0
        good_value = rule.value
        for cell in rule.cells:
            current_value += board[cell.row][cell.col]
        if current_value != good_value:
            return False
    return True


def sum_permutations(number_elems, sum_total):
    if number_elems == 1:
        yield (sum_total,)
    else:
        for i in range(1, sum_total):
            for j in sum_permutations(number_elems - 1, sum_total - i):
                yield (i,) + j


def get_new_candidates(rules, cnt_rule):
    rule = rules[cnt_rule]
    return sum_permutations(len(rule.cells), rule.value)


def apply_candidate(board, new_candidate, rules, cnt_rule):
    rule = rules[cnt_rule]
    count = 0
    for cell in rule.cells:
        board[cell.row][cell.col] = new_candidate[count]
        count += 1
    return board


def backtracking(board, rules, cnt_rule):
    if is_solution(board, rules):
        return (True, board)
    else:
        if cnt_rule < len(rules):
            new_candidates = get_new_candidates(rules, cnt_rule)
            for new_candidate in new_candidates:
                new_board = apply_candidate(board, new_candidate, rules, cnt_rule)
                solution = backtracking(new_board, rules, cnt_rule + 1)
                if solution[0]:
                    return solution
        return (False, None)


FRSTVALUE = ord('A')

# Get content from file
siz = len(sys.argv)
if siz < 2:
    print("usage: kakuro.py input.txt")
    sys.exit()

content = [line.rstrip('\n') for line in open(str(sys.argv[1]), 'r')]

# Process first line of file
firstline = content[0]
sizes = firstline.split(' ')
if len(sizes) < 2:
    print("Size configuration parameters are wrong")

size_cols = int(sizes[0])
size_rows = int(sizes[1])

cols = [chr(c) for c in range(FRSTVALUE, FRSTVALUE + size_cols)]
rows = [str(r) for r in range(1, 1 + size_rows)]

# Process second line of file
sum_params = content[1:]
sums = str(sum_params).split(' ')
if len(sums) < 2:
    print("Configuration cells  are wrong")

# Set up matr with values
rules = []
# rows x cols
for params in sum_params:
    params = params.split(' ')
    value = int(params[0])
    cells = []
    for posic in params[1:]:
        col = ord(str(posic)[0]) - FRSTVALUE
        row = int(str(posic)[1]) - 1
        cell = Cell(row, col)
        cells.append(cell)
    rules.append(Rule(value, cells))

init_board = [x[:] for x in [[0] * size_cols] * size_rows]

result = backtracking(init_board, rules, 0)
print("--------------------------")
print("cols: " + str(cols))
print("rows: " + str(rows))
print("rules: ")
for rule in rules:
    print(rule)

print("Board result: " + str(result))
print("--------------------------")