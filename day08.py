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


def get_steps(directions: str, nodes: dict[str: tuple[str,str]]) -> int:
    steps = 0

    curr_node, next_node = "AAA", ""
    while curr_node != "ZZZ":
        left, right = nodes[curr_node]

        step = steps % len(directions)
        choice = directions[step]
        match choice: 
            case "L":   next_node = left
            case "R":   next_node = right
            case  _ :   return -1

        # print(curr_node, next_node)
        curr_node = next_node
        steps += 1

    return steps


def calculate_results(input):
    instructions = file_to_instructions(input)
    # instructions = example_instructions
    # instructions = extra_example

    directions, nodes = parse_instructions(instructions)
    steps = get_steps(directions, nodes)

    return steps


if __name__ == "__main__":
    input = "input08.txt"
    output = calculate_results(input)

    print(f"Number of steps: {output}")
