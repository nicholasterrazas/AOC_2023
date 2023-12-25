from collections import defaultdict

example_universe = [
    "...#......",
    ".......#..",
    "#.........",
    "..........",
    "......#...",
    ".#........",
    ".........#",
    "..........",
    ".......#..",
    "#...#.....",
]


def file_to_universe(file):
    with open(file) as f:
        universe = f.readlines()
        return universe
    
def empty(line: list[str]):
    return [space == "." for space in line]


def rows(matrix: list[list[str]]) -> list[str]: 
    return [row for row in matrix]

def cols(matrix: list[list[str]]) -> list[str]:
    columns = []

    for i in range(len(matrix[0])): # iterate through columns first, then rows
        column = []
        for j in range(len(matrix)):
            column.append(matrix[j][i])
        columns.append(column)

    return columns
            

# same effect as cols
# source: https://www.geeksforgeeks.org/transpose-matrix-single-line-python/
def transpose(matrix: list[list[str]]): 
    return list(map(list, zip(*matrix)))


def insert_empty_rows(indexes: list[int], matrix: list[list[str]]) -> list[list[str]]:
    inserted = []
    
    for idx, row in enumerate(matrix):
        if idx in indexes:  
            inserted.append(row)    # insert an extra empty row
        inserted.append(row)        # copy the original row for every row

    return inserted


def insert_empty_cols(indexes: list[int], matrix: list[list[str]]) -> list[list[str]]:
    # below code works because "transpose(transpose(matrix)) == matrix" is True
    column_wise = transpose(matrix)
    inserted_cols = insert_empty_rows(indexes, column_wise)
    row_wise = transpose(inserted_cols)
    
    return row_wise


def standardize(matrix: list[list[str]], dimensions: tuple[int,int]) -> list[list[str]]:
    row_count, col_count = dimensions

    # standardize rows
    for row in matrix:
        difference = len(row) - col_count
        if difference != 0:
            row += ["." * difference]

    # standardize cols
    col_wise = transpose(matrix)
    for col in col_wise:
        difference = len(col) - row_count
        if difference != 0:
            col += ["." * difference]
    standardized = transpose(col_wise)
    
    return standardized
    

def expand_universe(universe: list[list[str]]) -> list[list[str]]:
    empty_rows = [idx for idx, row in enumerate(rows(universe)) if all(empty(row))]
    empty_cols = [idx for idx, col in enumerate(cols(universe)) if all(empty(col))]

    rows_inserted = insert_empty_rows(empty_rows, universe)
    cols_inserted = insert_empty_cols(empty_cols, rows_inserted)

    new_row_count = len(universe)    + len(empty_rows)
    new_col_count = len(universe[0]) + len(empty_cols)
    dimensions = new_row_count, new_col_count

    expanded_universe = standardize(cols_inserted, dimensions)
    return expanded_universe


def identify_galaxies(universe: list[list[str]]) -> tuple[list[list[str]], list[tuple[int,int]]]:
    galaxies = []

    for row, line in enumerate(universe):
        for col, char in enumerate(line):
            if char == "#":
                galaxies.append((row,col))
                universe[row][col] = str(len(galaxies))

    return universe, galaxies    


def big_bang(universe: list[list[str]]) -> tuple[list[list[str]], list[tuple[int,int]]]:
    big_universe = expand_universe(universe)
    labelled_universe, galaxies = identify_galaxies(big_universe)
    
    return labelled_universe, galaxies


def get_surrounding(position: tuple[int,int], matrix: list[list[str]]):
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    directions = [
        (-1, 0),
        ( 0, 1),
        ( 1, 0),
        ( 0,-1),
    ]

    row, col = position

    surrounding = []
    for direction in directions:
        rd, cd = direction
        rf, cf = row + rd, col + cd

        if (0 <= rf < num_rows) and (0 <= cf < num_cols):
            surrounding.append((rf,cf))

    return surrounding


# graph representation: adjacency list
# key: point, value: list of points
# note: distance from every point to adjacent points is 1, so is omitted for now
def to_graph(matrix: list[list[str]]) -> dict[tuple[int,int], list[tuple[int,int]]]:
    graph = {}
    
    for row, line in enumerate(matrix):
        for col, char in enumerate(line):
            position = row, col
            graph[position] = get_surrounding(position, matrix)
    
    return graph


# get point with lowest distance to source, that is also unvisited
def min_point(unvisited: set[tuple[int,int]], point_to_distance: dict[tuple[int,int], int | float]) -> tuple[int,int]:
    distance_to_point = defaultdict(list)
    
    distances = set()
    for point in unvisited:
        distance = point_to_distance[point]
        distance_to_point[distance].append(point)
        
        distances.add(distance)
        
    min_distance = min(distances)
    min_points = distance_to_point[min_distance]
    
    return min_points[0]


def dijkstra(source: tuple[int,int], graph: dict[tuple[int,int], list[tuple[int,int]]]) -> dict[tuple[int,int], int]:
    
    unvisited = set([point for point in graph])
    point_distances = {point: 0 if point == source else float('inf') for point in graph}

    while unvisited:
        current = min_point(unvisited, point_distances)
        unvisited.remove(current)

        neighbors = graph[current]
        for neighbor in neighbors:
            if neighbor not in unvisited: continue      # if point is visited, skip it

            calculated_distance = point_distances[current] + 1
            known_distance = point_distances[neighbor]
            
            point_distances[neighbor] = min(calculated_distance, known_distance)

    return point_distances


def get_distances(universe: list[list[str]], galaxies: list[tuple[int,int]]) -> dict[tuple[str,str], int]:
    
    uni_graph = to_graph(universe)
    # for point in uni_graph: print(point, uni_graph[point])

    distances = {}

    for galaxy in galaxies:        
        src_row, src_col = galaxy
        fst = universe[src_row][src_col]

        distance_to_others = dijkstra(galaxy, uni_graph)
        for other in galaxies:
            dst_row, dst_col = other
            snd = universe[dst_row][dst_col]

            distance = distance_to_others[other]

            distances[fst,snd] = distance
            
    # for k in distances: print(k, distances[k])
    return distances


def calculate_results(input):
    universe = [list(line.strip()) for line in file_to_universe(input)]
    universe = [list(line.strip()) for line in example_universe]
    for r in universe: print(r)

    expanded, galaxies = big_bang(universe)
    for r in expanded: print(r)    

    distances = get_distances(expanded, galaxies)
    shortest_distances = sum([distances[pair] for pair in distances])/2      # each pair exists twice, so we must divide by 2

    return shortest_distances


if __name__ == "__main__":
    input = "input11.txt"
    output = calculate_results(input)

    print(f"Sum of shortest distances: {output}")