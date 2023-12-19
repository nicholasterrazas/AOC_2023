
# represents the island type 
# contains number that island represents, and list of coordinates the island sits on
Coordinates = tuple[int, int]
Island = tuple[int, Coordinates]



def get_islands(schematic: list[str]) -> list[Island]:
    
    islands = []

    for y, line in list(enumerate(schematic)):      # number of line in file, line of txt file

        end = 0
        for x, symbol in list(enumerate(line)):     # number of char in line, char of line 

            if x < end: continue    # skip already seen numbers

            # if we see a number, keep checking to the right until the number ends 
            # record the numbers AND the coordinates in between
            if symbol.isdigit():
                
                num_string = ""
                coords = []

                curr_sym = symbol
                end = x

                while end < len(line) and curr_sym.isdigit():
                    num_string += curr_sym      # build number
                    
                    coords.append((end,y))      # update coordinates 
                    
                    end += 1                    # advance to next character
                    curr_sym = line[end]        # ^^^

                number = int(num_string)
                island = number, coords
                
                islands.append(island)               
                

    return islands


def next_to_symbol(island: Island, schematic: list[str]) -> bool:
    symbols = ['@','#','$','%','&','*','-','+','=','/']
    directions = [
        (0,1),      # N
        (1,1),      # NE
        (1,0),      # E
        (1,-1),     # SE
        (0,-1),     # S
        (-1,-1),    # SW
        (-1,0),     # W
        (-1,1),     # NW
    ]

    number, coords = island
    for coordinate in coords:
        
        xi, yi = coordinate
        for xm, ym in directions:

            xf, yf = xi + xm, yi + ym

            if not (0 <= xf < len(schematic[0]) and 0 <= yf < len(schematic)):      # skip out of bounds locations
                continue
            
            around = schematic[yf][xf]
            if around in symbols:
                return True
    
    # if we've checked around all the coordinates of an island, without seeing a symbol, the island is invalid
    return False
            
    

def calculate_result(file):
    example = [         # answer for example is 4361
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598..",
    ]

    with open(file) as f:
        schematic = f.readlines()
        schematic = [line.strip()+"." for line in schematic]


    islands = get_islands(schematic)
    # print(islands)
    
    valid_pieces = [island for island in islands if next_to_symbol(island, schematic)]
    # print(valid_pieces)

    result = sum([number for number, coords in valid_pieces])
    return result



if __name__ == "__main__":

    input = "input03.txt"
    output = calculate_result(input)

    print(f"Sum of part numbers: {output}")