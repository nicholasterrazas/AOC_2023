
example_almanac = [
    "seeds: 79 14 55 13",
    "",
    "seed-to-soil map:",
    "50 98 2",
    "52 50 48",
    "",
    "soil-to-fertilizer map:",
    "0 15 37",
    "37 52 2",
    "39 0 15",
    "",
    "fertilizer-to-water map:",
    "49 53 8",
    "0 11 42",
    "42 0 7",
    "57 7 4",
    "",
    "water-to-light map:",
    "88 18 7",
    "18 25 70",
    "",
    "light-to-temperature map:",
    "45 77 23",
    "81 45 19",
    "68 64 13",
    "",
    "temperature-to-humidity map:",
    "0 69 1",
    "1 0 69",
    "",
    "humidity-to-location map:",
    "60 56 37",
    "56 93 4",
]


def file_to_almanac(file):
    with open(file) as f:
        almanac = f.readlines()
        almanac = [line.strip() for line in almanac]
    
    return almanac

def parse_almanac(almanac: list[str]):
    seed_sec = almanac[0]
    colon = seed_sec.find(":") + 2
    seeds = [int(seed) for seed in seed_sec[colon:].split(" ")]
    
    for line_num, line in enumerate(almanac):
        if line.startswith("seed-to-soil"): seed_soil_start = line_num
        if line.startswith("soil-to-fertilizer"): soil_fertilizer_start = line_num
        if line.startswith("fertilizer-to-water"): fertilizer_water_start = line_num
        if line.startswith("water-to-light"): water_light_start = line_num
        if line.startswith("light-to-temperature"): light_temperature_start = line_num
        if line.startswith("temperature-to-humidity"): temperature_humidity_start = line_num
        if line.startswith("humidity-to-location"): humidity_location_start = line_num


    seed_soil_sec = almanac[seed_soil_start:soil_fertilizer_start]
    seed_soil = [[int(num) for num in line.split(" ")] for line in seed_soil_sec[1:-1]]
    
    soil_fertilizer_sec = almanac[soil_fertilizer_start:fertilizer_water_start] 
    soil_fertilizer = [[int(num) for num in line.split(" ")] for line in soil_fertilizer_sec[1:-1]] 
    
    fertilizer_water_sec = almanac[fertilizer_water_start:water_light_start]
    fertilizer_water = [[int(num) for num in line.split(" ")] for line in fertilizer_water_sec[1:-1]]
    
    water_light_sec = almanac[water_light_start:light_temperature_start]
    water_light = [[int(num) for num in line.split(" ")] for line in water_light_sec[1:-1]]
    
    light_temperature_sec = almanac[light_temperature_start:temperature_humidity_start]
    light_temperature = [[int(num) for num in line.split(" ")] for line in light_temperature_sec[1:-1]]
    
    temperature_humidity_sec = almanac[temperature_humidity_start:humidity_location_start]
    temperature_humidity = [[int(num) for num in line.split(" ")] for line in temperature_humidity_sec[1:-1]]
    
    humidity_location_sec = almanac[humidity_location_start:]
    humidity_location = [[int(num) for num in line.split(" ")] for line in humidity_location_sec[1:-1]] 


    return seeds, seed_soil, soil_fertilizer, fertilizer_water, water_light, light_temperature, temperature_humidity, humidity_location


def get_map(map: list[list[int]]) -> list[tuple[range, int]]:
    mappings = [] 
    
    for line in map:
        dst, src, length = line
        
        span = range(src, src + length)
        offset = dst - src

        mapping = span, offset
        mappings.append(mapping)
            
    return mappings
    

def seed_to_location(seed: int, maps: list[list[tuple[range, int]]]) -> int:
    origin = seed
    for map in maps:
        for mapping in map:
            span, offset = mapping

            if origin in span:
                mapped = origin + offset
                # print(origin, mapped)
                origin = mapped
                break  
    # print()
    return mapped


def calculate_results(input):
    almanac = file_to_almanac(input)
    # almanac = example_almanac
    
    seeds, seed_soil, soil_fertilizer, fertilizer_water, water_light, light_temperature, temperature_humidity, humidity_location = parse_almanac(almanac)
    
    ss = get_map(seed_soil)
    sf = get_map(soil_fertilizer)
    fw = get_map(fertilizer_water)
    wl = get_map(water_light)
    lt = get_map(light_temperature)
    th = get_map(temperature_humidity)
    hl = get_map(humidity_location)
    
    maps = [ss,sf,fw,wl,lt,th,hl]
    min_location = min([seed_to_location(seed, maps) for seed in seeds]) 
    
    return min_location


if __name__ == "__main__":
    input = "input05.txt"
    output = calculate_results(input)

    print(f"Lowest location number: {output}")