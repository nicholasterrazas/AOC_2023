
def find_first(line: str) -> str:
    
    for character in line:
        if character.isdigit():
            return character
        
def find_last(line: str) -> str:
    enil = reversed(line)

    for character in enil:
        if character.isdigit():
            return character



def find_calibration_values(file) -> int:
    calibration_values = []    

    with open(file) as f:

        for line in f.readlines():
            fst = find_first(line)
            lst = find_last(line)

            cal_val = fst + lst     # concatenation, not addition
            calibration_values.append(cal_val)


    cal_vals = [int(val) for val in calibration_values]    
    return sum(cal_vals)


if __name__ == "__main__":

    input = "input01.txt"
    output = find_calibration_values(input)
    
    print(output)