example_dataset = [
    "0 3 6 9 12 15",
    "1 3 6 10 15 21",
    "10 13 16 21 30 45",
]

def file_to_histories(file):
    with open(file) as f:
        histories = f.readlines()
        return histories


def extrapolate(nums: list[int]) -> int:
    # base case:
    if all([n == 0 for n in nums]): return 0
    
    # recursive case:
    differences = []
    for i in range(1, len(nums)):
        prev = nums[i-1]
        curr = nums[i]
        
        diff = curr - prev
        differences.append(diff)

    return nums[-1] + extrapolate(differences)
    

def predictions(histories: list[list[int]], predictions: list[int]) -> list[list[int]]:
    return [his + [pred] for his, pred in zip(histories, predictions)]


def calculate_results(input):
    dataset = file_to_histories(input)
    # dataset = example_dataset

    histories = [[int(num) for num in history.split(" ")] for history in dataset]
    extrapolated_values = [extrapolate(history) for history in histories]
    # for pred in predictions(histories, extrapolated_values): print(pred)

    return sum(extrapolated_values)


if __name__ == "__main__":
    input = "input09.txt"
    output = calculate_results(input)

    print(f"Sum of extrapolated values: {output}")