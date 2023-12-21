example_records = [
    "Time:      7  15   30",
    "Distance:  9  40  200",
]

def file_to_records(file):
    with open(file) as f:
        records = f.readlines()
        return records


def parse_records(records: list[str]):
    time_section = records[0]
    distance_section = records[1]

    t_col = time_section.find(":") + 1
    d_col = distance_section.find(":") + 1

    times = [int(num) for num in time_section[t_col:].split(" ") if num != ""]
    distances = [int(num) for num in distance_section[d_col:].split(" ") if num != ""]

    return times, distances


def get_win_range(race_time: int, race_distance: int) -> range:
    
    # two pointer solution, for big ranges
    start, finish = -1, -1
    for present_time in range(race_time):
        charge_duration = present_time
        
        speed = charge_duration
        time_left = race_time - present_time
        distance_travelled = speed * time_left
        
        if distance_travelled > race_distance:
            start = charge_duration
            break
        
    for present_time in reversed(range(race_time)):
        charge_duration = present_time
        
        speed = charge_duration
        time_left = race_time - present_time
        distance_travelled = speed * time_left

        if distance_travelled > race_distance:
            finish = charge_duration + 1
            break

    winners = range(start, finish)
    return winners


def product(xs: list[int]) -> int:
    Π = 1
    for x in xs:
        Π *= x
    return Π


def calculate_results(input):
    records = file_to_records(input)
    # records = example_records
    
    times, distances = parse_records(records)
    win_margins = [get_win_range(time, distance) for time, distance in zip(times, distances)]
    margin_product = product([len(margin) for margin in win_margins])

    actual_time = ""
    for t in times: actual_time += str(t)

    actual_distance = ""
    for d in distances: actual_distance += str(d)
    
    actual_time, actual_distance = int(actual_time), int(actual_distance)
    actual_margin = get_win_range(actual_time, actual_distance)

    return margin_product, len(actual_margin)


if __name__ == "__main__":
    input = "input06.txt"
    output = calculate_results(input)

    print(f"Win margins product: {output[0]}, Actual win margins product: {output[1]}")