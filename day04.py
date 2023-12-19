def file_to_pile(file) -> list[str]:
    with open(file) as f:
        board = f.readlines()
        return board
    

def parse_card(card: str):
    card = card.strip()

    colon = card.find(":") + 1
    pipe = card.find("|") + 1

    winners = card[colon:pipe].split(" ")
    owned = card[pipe:].split(" ")

    winners = [int(win) for win in winners if win.isdigit()]
    owned = [int(own) for own in owned if own.isdigit()]

    return winners, owned
    

def get_points(card: str) -> int:
    winners, owned = parse_card(card)

    win_count = 0
    for num in owned:
        if num in winners:
            win_count += 1
    
    points = 0 if win_count == 0 else 2 ** (win_count - 1)
    return points


def calculate_results(input: str) -> int:
    pile = file_to_pile(input)
    total_points = sum([get_points(card) for card in pile])
    return total_points


if __name__ == "__main__":

    input = "input04.txt"
    output = calculate_results(input)

    print(f"Sum of points of cards in pile: {output}")