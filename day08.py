from math import lcm

example_instructions = [
    "RL",
    "",
    "AAA = (BBB, CCC)",
    "BBB = (DDD, EEE)",
    "CCC = (ZZZ, GGG)",
    "DDD = (DDD, DDD)",
    "EEE = (EEE, EEE)",
    "GGG = (GGG, GGG)",
    "ZZZ = (ZZZ, ZZZ)",
]

extra_example = [
    "LLR",
    "",
    "AAA = (BBB, BBB)",
    "BBB = (AAA, ZZZ)",
    "ZZZ = (ZZZ, ZZZ)",
]

ghost_instructions = [
    "LR",
    "",
    "11A = (11B, XXX)",
    "11B = (XXX, 11Z)",
    "11Z = (11B, XXX)",
    "22A = (22B, XXX)",
    "22B = (22C, 22C)",
    "22C = (22Z, 22Z)",
    "22Z = (22B, 22B)",
    "XXX = (XXX, XXX)",
]

def file_to_instructions(file):
    with open(file) as f:
        instructions = f.readlines()
        return instructions
    
def parse_instructions(instructions: list[str]) -> tuple[str, dict[str, tuple[str,str]]]:
    directions = instructions[0].strip()
    map_section = instructions[2:]

    nodes = {}
    for line in map_section:
        label = line[0:3]

        left = line[7:10]
        right = line[12:15]

        nodes[label] = left, right

    return directions, nodes


def get_steps(start, directions: str, nodes: dict[str: tuple[str,str]]) -> int:
    steps = 0

    location = start
    while location[-1] != "Z":
        step = steps % len(directions)
        choice = directions[step]
        
        location = get_path(location, choice, nodes)

        steps += 1

    return steps


def is_end(node: str) -> bool:
    return True if node[-1] == "Z" else False

def all_done(nodes: list[str]) -> bool:
    ends = [is_end(node) for node in nodes]
    # print(ends)
    return all(ends)


def get_ghost_steps(directions: str, nodes: dict[str: tuple[str,str]]) -> int:
    ghost_steps = 0

    locations = [node for node in nodes if node[-1] == "A"]     # get all starting nodes
    while not all_done(locations):
        step = ghost_steps % len(directions)
        choice = directions[step]

        locations = [get_path(location, choice, nodes) for location in locations]

        ghost_steps += 1

    return ghost_steps


def get_path(location: str, choice: str, nodes: dict[str, tuple[str,str]]) -> str:
    left, right = nodes[location]
    match choice:
        case "L":   path = left
        case "R":   path = right
        case  _ :   path = "ERROR"
    return path


def calculate_results(input):
    instructions = file_to_instructions(input)
    # instructions = example_instructions
    # instructions = extra_example
    # instructions, steps = ghost_instructions, 0

    directions, nodes = parse_instructions(instructions)
    steps = get_steps("AAA", directions, nodes)

    # apparently, ghost steps can be given by getting the LCM of all the ghost path lengths
    # ghost_steps = get_ghost_steps(directions, nodes)  # took too long to run
    ghosts = [path for path in nodes if path[-1] == "A"]
    ghost_steps = [get_steps(ghost, directions, nodes) for ghost in ghosts]

    return steps, lcm(*ghost_steps)


if __name__ == "__main__":
    input = "input08.txt"
    output = calculate_results(input)

    print(f"Number of steps: {output[0]}, Number of ghost steps: {output[1]}")
