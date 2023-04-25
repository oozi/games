from collections import Counter

def get_easy_sudoku():
    """This can be solved using single digit elimination only"""

    grid = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)]

    grid[0][0] = [5]
    grid[0][2] = [2]
    grid[0][3] = [3]
    grid[0][5] = [1]
    grid[0][6] = [6]

    grid[1][0] = [9]
    grid[1][5] = [4]
    grid[1][6] = [7]
    grid[1][8] = [3]

    grid[2][0] = [8]
    grid[2][5] = [6]
    grid[2][6] = [2]
    grid[2][8] = [5]

    grid[3][1] = [5]
    grid[3][3] = [2]
    grid[3][4] = [7]
    grid[3][7] = [6]

    grid[4][1] = [3]
    grid[4][2] = [8]
    grid[4][3] = [1]
    grid[4][5] = [9]
    grid[4][6] = [4]

    grid[5][1] = [6]
    grid[5][7] = [2]
    grid[5][8] = [9]

    grid[6][2] = [1]
    grid[6][3] = [4]
    grid[6][4] = [5]

    grid[7][2] = [4]
    grid[7][5] = [8]
    grid[7][6] = [5]
    grid[7][7] = [3]
    grid[7][8] = [2]

    grid[8][1] = [2]
    grid[8][2] = [5]
    grid[8][4] = [3]
    grid[8][6] = [8]
    grid[8][7] = [4]

    return grid


def get_medium_sudoku():
    grid = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)]

    grid[0][5] = [3]

    grid[1][1] = [7]
    grid[1][3] = [8]
    grid[1][6] = [2]

    grid[2][0] = [9]
    grid[2][1] = [8]
    grid[2][4] = [6]
    grid[2][7] = [1]

    grid[3][8] = [6]

    grid[4][0] = [6]
    grid[4][1] = [2]
    grid[4][2] = [4]
    grid[4][6] = [8]

    grid[5][1] = [5]
    grid[5][5] = [9]

    grid[6][1] = [9]
    grid[6][4] = [4]
    grid[6][8] = [1]

    grid[7][1] = [1]
    grid[7][2] = [5]
    grid[7][4] = [9]
    grid[7][7] = [2]
    grid[7][8] = [3]

    grid[8][4] = [8]

    return grid


def get_3x3_str(lst, show_candidates=True):
    lst.sort()
    padded_list = [" "] * 9
    if len(lst) == 1:
        padded_list[4] = str(lst[0])
    else:
        if not show_candidates:
            return [" "*5, " "*5, " "*5]
        for i in lst:
            idx = i-1
            padded_list[idx] = str(i)

    rows = [" ".join(padded_list[:3]), " ".join(padded_list[3:6]), " ".join(padded_list[6:])]

    return rows


def print_grid(grid, show_candidates=True):
    print("-" * 73)
    for row in grid:
        element_lines = [get_3x3_str(element, show_candidates=show_candidates) for element in row]
        for i in range(3):
            grid_lines = [line[i] for line in element_lines]
            print("|", " | ".join(grid_lines), "|")
        print("-" * 73)


def single_values(grid):
    coordinates = []
    for i, row in enumerate(grid):
        for j, element in enumerate(row):
            if len(element) == 1:
                coordinates.append((i, j))
    return coordinates


def remove_values_from_row(grid, row_n, values):
    change_made = False
    for lst in grid[row_n]:
        if len(lst) > len(values):
            for value in values:
                if value in lst:
                    lst.remove(value)
                    change_made = True
    return change_made


def remove_values_from_col(grid, col_n, values):
    change_made = False
    for row_n in range(len(grid)):
        lst = grid[row_n][col_n]
        if len(lst) > len(values):
            for value in values:
                if value in lst:
                    lst.remove(value)
                    change_made = True
    return change_made


def get_box_number(row, col):
    box_i = (row) // 3
    box_j = (col) // 3
    box_number = box_i * 3 + box_j + 1
    return box_number


def get_coordinates_from_box_number(box_number):
    box_x = (box_number - 1) % 3
    box_y = (box_number - 1) // 3
    coordinates = []

    for i in range(3):
        for j in range(3):
            col = box_x * 3 + i
            row = box_y * 3 + j
            coordinates.append((row, col))

    return coordinates


def remove_values_from_box(grid, box_n, values):
    change_made = False
    coordinates = get_coordinates_from_box_number(box_n)
    for row, col in coordinates:
        lst = grid[row][col]
        if len(lst) > len(values):
            for value in values:
                if value in lst:
                    lst.remove(value)
                    change_made = True
    return change_made


def single_eliminations(grid):
    change_made = False
    for i in range(9):
        for j in range(9):
            lst = grid[i][j]
            if len(lst) == 1:
                box_n = get_box_number(i, j)
                is_row_changed = remove_values_from_row(grid, i, lst)
                is_col_changed = remove_values_from_col(grid, j, lst)
                is_box_changed = remove_values_from_box(grid, box_n, lst)
                if is_row_changed or is_col_changed or is_box_changed:
                    change_made = True

    return change_made


def is_sudoku_solved(grid):
    expected_values = {*list(range(1, 10))}
    for i in range(9):
        for j in range(9):
            if len(grid[i][j]) != 1:
                return False
        if ({grid[i][k][0] for k in range(9)} != expected_values
            or {grid[j][k][0] for k in range(9)} != expected_values
            or {grid[x][y][0] for x, y in get_coordinates_from_box_number(i+1)} != expected_values):
            return False
        get_coordinates_from_box_number(i+1)
    return True


def double_eliminations(grid):
    change_made = False
    for i in range(9):
        row_doubles = [list(k) for k, v in Counter([tuple(grid[i][j]) for j in range(9) if len(grid[i][j]) == 2]).items() if v == 2]
        col_doubles = [list(k) for k, v in Counter([tuple(grid[j][i]) for j in range(9) if len(grid[j][i]) == 2]).items() if v == 2]
        box_doubles = [list(k) for k, v in Counter([tuple(grid[x][y]) for x, y in get_coordinates_from_box_number(i+1) if len(grid[x][y]) == 2]).items() if v == 2]

        if row_doubles:
            for double in row_doubles:
                print(f"row {i}, {double}")
                if remove_values_from_row(grid, i, double):
                    change_made = True

        if col_doubles:
            for double in col_doubles:
                print(f"col {i}, {double}")
                if remove_values_from_col(grid, i, double):
                    change_made = True

        if box_doubles:
            for double in box_doubles:
                print(f"box {i+1}, {double}")
                if remove_values_from_box(grid, i+1, double):
                    change_made = True

    return change_made


grid = get_medium_sudoku()
print("before:")
print_grid(grid, show_candidates=False)



while True:
    single_elims = False
    double_elims = False
    while single_eliminations(grid):
        single_elims = True

    while double_eliminations(grid):
        double_elims = True

    if not single_elims and not double_elims:
        break

print_grid(grid)

# while single_eliminations(grid):
#     pass

# while double_eliminations(grid):
#     pass

# print_grid(grid)



# if is_sudoku_solved(grid):
#     print("after:")
#     print_grid(grid)
