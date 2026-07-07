import sys

def read_input(input_file_path ,output_file_path):
    with open(input_file_path, "r") as file:
        lines = file.readlines()
    costs = list(map(int, lines[0].split()))
    grid = [list(map(int, line.split())) for line in lines[1:]]

    best_grid , best_cost = find_best_path(grid, calculate_costs, costs)
    write_output(output_file_path, best_cost, best_grid)

    return costs, grid


def write_output(file_path, costs, grid):
    with open(file_path, "w") as file:
        if costs == 0:
            file.write("There is no possible route!")
        else:
            file.write(f"Cost of the route: {costs}\n")
            for row in grid:
                file.write(" ".join(map(str, row)) + "\n")



def process_grid_recursive(grid, n, m, costs):
    rows = len(grid)
    cols = len(grid[0])

    # rightmost column
    if m == cols - 1:
        return True

    # control directions according to movement priority order
    best_cost = float('inf')
    best_move = None

    # check the right first, find the cost value
    if m + 1 < cols and grid[n][m + 1] == 1:
        grid[n][m] = "X"
        grid[n][m + 1] = "X"
        current_cost = calculate_costs(grid, costs)
        grid[n][m] = 1
        grid[n][m + 1] = 1
        if current_cost < best_cost:
            best_cost = current_cost
            best_move = (n, m + 1)

    # check above, if the cost value is smaller, take this as the best move
    if n - 1 >= 0 and grid[n - 1][m] == 1:
        grid[n][m] = "X"
        grid[n - 1][m] = "X"
        current_cost = calculate_costs(grid, costs)
        grid[n][m] = 1
        grid[n - 1][m] = 1
        if current_cost < best_cost:
            best_cost = current_cost
            best_move = (n - 1, m)

    # check below, if the cost value is smaller, take this as the best move
    if n + 1 < rows and grid[n + 1][m] == 1:
        grid[n][m] = "X"
        grid[n + 1][m] = "X"
        current_cost = calculate_costs(grid, costs)
        grid[n][m] = 1
        grid[n + 1][m] = 1
        if current_cost < best_cost:
            best_cost = current_cost
            best_move = (n + 1, m)

    # check left, if cost value is smaller take this as best move
    if m - 1 >= 0 and grid[n][m - 1] == 1:
        grid[n][m] = "X"
        grid[n][m - 1] = "X"
        current_cost = calculate_costs(grid, costs)
        grid[n][m] = 1
        grid[n][m - 1] = 1
        if current_cost < best_cost:
            best_cost = current_cost
            best_move = (n, m - 1)

    if best_move:
        next_n, next_m = best_move
        grid[n][m] = "X"
        grid[next_n][next_m] = "X"
        if process_grid_recursive(grid, next_n, next_m, costs):
            return True


    return False  # if there is no possible movement


def process_grid(grid, start_row, costs):
    if grid[start_row][0] == 1:   # we will use the "start row" value to check the sub-rows
        if process_grid_recursive(grid, start_row, 0, costs):
            return grid
    return grid

def calculate_costs(grid, costs):
    rows = len(grid)
    cols = len(grid[0])
    cost1 = costs[0]
    cost2 = costs[1]
    cost3 = costs[2]
    c1 = 0
    c2 = 0
    c3 = 0
    for n in range(rows):
        for m in range(cols):
            if grid[n][m] == "X":
                horizontal_vertical = False
                diagonal = False

                # up
                if n - 1 >= 0 and grid[n - 1][m] == 0:
                    horizontal_vertical = True
                # above
                if n + 1 < rows and grid[n + 1][m] == 0:
                    horizontal_vertical = True
                # left
                if m - 1 >= 0 and grid[n][m - 1] == 0:
                    horizontal_vertical = True
                # right
                if m + 1 < cols and grid[n][m + 1] == 0:
                    horizontal_vertical = True
                # Upper left cross
                if n - 1 >= 0 and m - 1 >= 0 and grid[n - 1][m - 1] == 0:
                    diagonal = True
                # Upper right cross
                if n - 1 >= 0 and m + 1 < cols and grid[n - 1][m + 1] == 0:
                    diagonal = True
                # Lower left cross
                if n + 1 < rows and m - 1 >= 0 and grid[n + 1][m - 1] == 0:
                    diagonal = True
                # Lower right cross
                if n + 1 < rows and m + 1 < cols and grid[n + 1][m + 1] == 0:
                    diagonal = True


                if horizontal_vertical:
                    c3 += cost3
                elif diagonal:
                    c2 += cost2
                else:
                    c1 += cost1
    return c1+c2+c3

def find_best_path(grid, calculate_costs, costs):
    rows = len(grid)
    best_cost = float('inf')
    best_path = None

    # we also check the lower left rows
    for start_row in range(rows):
        if grid[start_row][0] == 1:
            gridd = [row[:] for row in grid]  # We copy the grid not to lose it
            processed_grid = process_grid(gridd, start_row, costs)
            cost = calculate_costs(processed_grid, costs)
            if cost < best_cost:
                best_cost = cost
                best_path = [row[:] for row in processed_grid]

    # If the cost value is smaller, it starts from that row
    if best_path:
        return best_path , best_cost

    return grid





if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Sample run command: python3 route_finder.py <input_file> <output_file>")
    else:
        input_file_path = sys.argv[1]
        output_file_path = sys.argv[2]
        read_input(input_file_path, output_file_path)