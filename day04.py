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
    

def get_win_count(card: str):
    winners, owned = parse_card(card)

    win_count = 0
    for num in owned:
        if num in winners:
            win_count += 1

    return win_count


def get_points(card: str) -> int:
    win_count = get_win_count(card)    
    points = 0 if win_count == 0 else 2 ** (win_count - 1)
    return points


def get_copies(pile: list[str]) -> str:    
    copies_won = {}      # key: card id, value: list of ids of cards that card id won
    for card_id, card in enumerate(pile):
        points = get_win_count(card)
        if points > 0:
            copies_won[card_id] = list(range(card_id+1, card_id+points+1))

    copy_ids = list(range(len(pile)))
    for card_id in range(len(pile)):
        # scan through the copy ids: 
        # if we encounter the current card, retrieve the copies it won and add them
        occurences = 0
        for copy_id in copy_ids:
            if copy_id == card_id:
                occurences += 1

        additional_copies = copies_won.get(card_id, []) * occurences
        copy_ids += additional_copies


    copies = [pile[copy_id] for copy_id in copy_ids]
    return copies


def calculate_results(input: str) -> int:
    example = [
        "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
        "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
        "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
        "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
        "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
        "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
    ]

    pile = file_to_pile(input)

    total_points = sum([get_points(card) for card in pile])
    
    copies = get_copies(pile)
    copy_count = len(copies)

    return total_points, copy_count


if __name__ == "__main__":

    input = "input04.txt"
    output = calculate_results(input)

    print(f"Sum of points of cards in pile: {output[0]}, Total scratch cards won: {output[1]}")