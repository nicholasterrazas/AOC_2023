
def parse_details(details: str):
    col = details.index(":")
    
    id = int(details[4:col])                # exclude "Game" and everything after the colon
    reveal_section = details[col+1:]        # exclude "Game X:", only includes info about reveals
    
    r,g,b = 0,0,0   # red count, green count, blue count

    # reveal_str example: "9 blue, 13 green, 1 red"        
    reveal_strings = reveal_section.split(";")
    for reveal_str in reveal_strings:   
        
        # color_str example: "9 blue"
        colors = reveal_str.split(",")
        for color_str in colors:
            color_str = color_str.strip()

            sections = color_str.split(" ")
            count = int(sections[0])
            color = sections[1]

            if color == "red":
                r = max(r, count)
            elif color == "green":
                g = max(g, count)
            elif color == "blue":
                b = max(b, count)
            else:
                print(sections)

    return (id, r, g, b)
            

def game_to_stats(details: str):
    stats = parse_details(details)
    return stats



def find_games(file, sieve):
    
    def less_than(stat):
        max_r, max_g, max_b = sieve
        id, r, g, b = stat

        if r <= max_r and g <= max_g and b <= max_b:
            return True
        else:
            return False

    with open(file) as f:

        stats = []
        for game in f.readlines():

            game_stat = game_to_stats(game)
            stats.append(game_stat)

    valid_games = list(filter(less_than, stats))                        
    result = sum([id for id,r,g,b in valid_games])      # sum of IDs of valid games

    return result



if __name__ == "__main__":

    # filename, filter = games with <= 12 R, <= 13 G, <= 14 B
    input = "input02.txt"
    output = find_games(input, (12,13,14))

    print(output)