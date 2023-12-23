
example_0 = [
    ".....",
    ".S-7.",
    ".|.|.",
    ".L-J.",
    ".....",
]

example_1 = [
    "-L|F7",
    "7S-7|",
    "L|7||",
    "-L-J|",
    "L|-JF",
]

example_2 = [
    "..F7.",
    ".FJ|.",
    "SJ.L7",
    "|F--J",
    "LJ...",
]

example_3 = [
    "7-F7-",
    ".FJ|7",
    "SJLL7",
    "|F--J",
    "LJ.LJ",
]




def file_to_maze(file):
    with open(file) as f:
        maze = f.readlines()
        maze = [list(row) for row in maze]
        return maze


loc = tuple[int, int]   # location type: (row, col)


def find_animal(maze: list[list[str]]) -> loc:
    for row, line in enumerate(maze):
        for col, char in enumerate(line):
            if maze[row][col] == "S": 
                return (row,col)


def find_paths(animal_location: loc, maze: list[list[str]]) -> tuple[loc, loc]:
    directions = {
        (-1,  0): ["|","7","F"],    # N
        ( 0,  1): ["-","J","7"],    # E
        ( 1,  0): ["|","J","L"],    # S
        ( 0, -1): ["-","L","F"],    # W
    }

    paths = []  # should only contain two locations at the end

    row_start, col_start = animal_location
    for direction in directions:
        row_shift, col_shift = direction
        row_final, col_final = row_start + row_shift, col_start + col_shift 
        
        final_path = maze[row_final][col_final]
        valid_routes = directions[direction]

        if final_path in valid_routes:
            paths.append((row_final, col_final))

    return paths


def get_movement(prev_pos: loc, curr_pos: loc):
    row_start, col_start = prev_pos
    row_final, col_final = curr_pos
    movement = row_start - row_final, col_start - col_final
    
    return movement


def translate_movement(movement: tuple[int,int]) -> str:
    match movement:
        case -1,  0: return "N"
        case  0,  1: return "E"
        case  1,  0: return "S"
        case  0, -1: return "W"
        case  _,  _: return f"ERROR: {movement}"
    

def get_destination(tile: str, movement: tuple[int,int]) -> tuple[int,int]:
        src = tile, movement
        match src:
            case "|", "N": dst = ( 1,  0)   # came from North, move South
            case "J", "N": dst = ( 0, -1)   # came from North, move West
            case "L", "N": dst = ( 0,  1)   # came from North, move East
            
            case "-", "E": dst = ( 0, -1)   # came from East,  move West
            case "L", "E": dst = (-1,  0)   # came from East,  move North
            case "F", "E": dst = ( 1,  0)   # came from East,  move South 
            
            case "|", "S": dst = (-1,  0)   # came from South, move North
            case "7", "S": dst = ( 0, -1)   # came from South, move West
            case "F", "S": dst = ( 0,  1)   # came from South, move East
            
            case "-", "W": dst = ( 0,  1)   # came from West,  move East
            case "J", "W": dst = (-1,  0)   # came from West,  move North
            case "7", "W": dst = ( 1,  0)   # came from West,  move South
            
            case _:
                print(movement, tile)
                return None

        return dst    


def next_position(curr_pos: loc, movement: tuple[int,int], maze: list[list[str]]) -> loc:
    curr_row, curr_col = curr_pos
    tile = maze[curr_row][curr_col]

    row_shift, col_shift = get_destination(tile, translate_movement(movement))

    next_row, next_col = curr_row + row_shift, curr_col + col_shift
    next_pos = next_row, next_col
    
    return next_pos


def travel_path(curr_pos: loc, travelled: list[loc], maze: list[list[str]]) -> list[loc]:
    row, col = curr_pos
    tile = maze[row][col]

    # base case
    if tile == "S": return travelled

    # recursive case
    prev_pos = travelled[-1]
    movement = get_movement(prev_pos, curr_pos)
    next_pos = next_position(curr_pos, movement, maze)

    travelled.append(curr_pos)
    return travel_path(next_pos, travelled, maze)


def get_furthest_point(path1: list[loc], path2: list[loc]):
    
    for idx, (loc1, loc2) in enumerate(zip(path1[1:], path2[1:])):
        if loc1 == loc2: 
            return idx+1


def calculate_results(input):
    maze = file_to_maze(input)
    maze = example_0
    maze = example_1
    maze = example_2
    maze = example_3

    animal_location = find_animal(maze)
    nearby = find_paths(animal_location, maze)

    path1, path2 = [travel_path(location, [animal_location], maze) for location in nearby]
    furthest = get_furthest_point(path1, path2)

    return furthest


if __name__ == "__main__":
    input = "input10.txt"
    output = calculate_results(input)

    print(f"Furthest point: {output}")