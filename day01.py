
def first_digit_num(line: str):
    
    for idx in range(len(line)):
        character = line[idx]
        if character.isdigit():
            return character, idx
        
def last_digit_num(line: str):
    enil = list(reversed(line))

    for idx in range(len(enil)):
        character = enil[idx]
        if character.isdigit():
            return character, (len(enil) - idx) -1


str_to_num = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

def first_string_num(line: str):
    nums = ['one','two','three','four','five','six','seven','eight','nine']
    pos_to_num = {line.find(num): num for num in nums if line.find(num) != -1}
    positions = pos_to_num.keys()

    if len(positions) == 0:
        return None, None

    idx = min(positions)                # location of earliest number in line 
    fst = str_to_num[pos_to_num[idx]]   # actual number in line

    return fst, idx

def last_string_num(line: str):
    nums = ['one','two','three','four','five','six','seven','eight','nine']
    pos_to_num = {line.rfind(num): num for num in nums if line.rfind(num) != -1}     # note: usage of rfind() vs find()
    positions = pos_to_num.keys()
    
    if len(positions) == 0:
        return None, None
    
    idx = max(positions)                # location of earliest number in line 
    lst = str_to_num[pos_to_num[idx]]   # actual number in line

    return lst, idx


def get_calibration_value(line: str):
    
    first_digit, first_digit_idx = first_digit_num(line)
    last_digit, last_digit_idx = last_digit_num(line)

    first_string, first_string_idx = first_string_num(line)
    last_string, last_string_idx = last_string_num(line)


    if not first_string:    # no first string implies no last string, AKA NO string numbers in line 
        cal_val = (first_digit + last_digit)
    else: 
        fst = first_digit if first_digit_idx < first_string_idx else first_string
        lst = last_digit if last_digit_idx > last_string_idx else last_string
        cal_val = (fst + lst)    # concatenation, not addition
    
    # print(line, first_digit, first_digit_idx, last_digit, last_digit_idx, first_string, first_string_idx, last_string, last_string_idx, cal_val)
    
    return cal_val


def find_calibration_values(file) -> int:
    calibration_values = []    

    with open(file) as f:

        for line in f.readlines():
            cal_val = get_calibration_value(line)
            calibration_values.append(cal_val)


    cal_vals = [int(val) for val in calibration_values]    
    # print(cal_vals)
    return sum(cal_vals)


if __name__ == "__main__":

    input = "input01.txt"
    output = find_calibration_values(input)
    
    print(output)