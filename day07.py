from collections import Counter

# source: "https://adventofcode.com/2023/day/7"
example_camel_cards = [
    "32T3K 765",
    "T55J5 684",
    "KK677 28",
    "KTJJT 220",
    "QQQJA 483",
]

# source: "https://www.reddit.com/r/adventofcode/comments/18cr4xr/2023_day_7_better_example_input_not_a_spoiler/"
better_example = [
    "2345A 1",
    "Q2KJJ 13",
    "Q2Q2Q 19",
    "T3T3J 17",
    "T3Q33 11",
    "2345J 3",
    "J345A 2",
    "32T3K 5",
    "T55J5 29",
    "KK677 7",
    "KTJJT 34",
    "QQQJA 31",
    "JJJJJ 37",
    "JAAAA 43",
    "AAAAJ 59",
    "AAAAA 61",
    "2AAAA 23",
    "2JJJJ 53",
    "JJJJ2 41",
]


def file_to_cards(file):
    with open(file) as f:
        camel_cards = f.readlines()
        return camel_cards


def parse_cards(cards: list[str]) -> [tuple[str, int]]:
    hands, bids = [], []
    for card in cards:
        sections = card.split(" ")
        hand = sections[0]
        bid = int(sections[1])

        hands.append(hand)
        bids.append(bid)

    return hands, bids


# standardizes hands into list of frequencies of cards
def hand_to_frequencies(hand: str) -> list[int]:
    sorted_cards = "".join(sorted(hand))
    frequencies = [frequency for card, frequency in Counter(sorted_cards).most_common()]
    
    return frequencies


# cache = {}
def get_strength(hand: str) -> int:
    # 5 cards same type:                            strength = 6, types = 1
    # 4 cards same, 1 off:                          strength = 5, types = 2
    # 3 cards same, 2 different same:               strength = 4, types = 2
    # 3 cards same, others different:               strength = 3, types = 3
    # 2 cards same, 2 others same, one different:   strength = 2, types = 3
    # 2 cards same, others different:               strength = 1, types = 4
    # all cards different:                          strength = 0, types = 5

    freqs = hand_to_frequencies(hand)
    # if cache.get(str(freqs)) is not None:
    #     return cache[str(freqs)]

    types = len(freqs)
    if types == 5:          strength = 0
    elif types == 4:        strength = 1
    elif types == 3:
        fst, snd, trd = freqs
        match fst,snd,trd:
            case 2,2,1:     strength = 2
            case 3,1,1:     strength = 3
    elif types == 2:
        fst, snd = freqs
        match fst, snd:
            case 3,2:       strength = 4
            case 4,1:       strength = 5
    elif types == 1:        strength = 6
    else:                   # shouldn't reach here
        print(f"{hand}, {freqs}")       
        strength = -1

    # cache[str(freqs)] = strength
    return strength


def card_value(card: str) -> int:

    match card:
        case "1":   value = 1
        case "2":   value = 2
        case "3":   value = 3
        case "4":   value = 4
        case "5":   value = 5
        case "6":   value = 6
        case "7":   value = 7
        case "8":   value = 8
        case "9":   value = 9
        case "T":   value = 10
        case "K":   value = 11
        case "Q":   value = 12
        case "J":   value = 13
        case "A":   value = 14
        case _:     value = -1

    return value


def sort_hand(hand: str) -> list[int]:
    card_list = [card_value(card) for card in hand]
    # print(card_list)
    return card_list


def rank_hands(hands: list[str]) -> dict[str,int]:
    ranks = {}

    strengths = [get_strength(hand) for hand in hands]
    hand_strengths = list(zip(hands, strengths))
    # print(hand_strengths)

    hand_strengths.sort(key=(lambda x: sort_hand(x[0])))    # sort by cards in hand
    # print(hand_strengths)

    hand_strengths.sort(key=(lambda x: x[1]))               # sort by strength 
    # print(hand_strengths)

    ranks = {hand: idx+1 for idx, (hand, strength) in enumerate(hand_strengths)}
    return ranks    


def print_stats(ranks: dict[str, int], hands: list[str], bids: list[int]) -> list[tuple[int, str, int, int]]:
    stats = list(zip([ranks[hand] for hand in hands], hands, bids, [get_strength(hand) for hand in hands]))
    stats.sort(key=lambda x: x[0])
    
    print("Rank\tHand\tBid\tStrength")
    print("================================")
    for rank, hand, bid, strength in stats:
        print(f"{rank}\t{hand}\t{bid}\t{strength}")

    return stats


    
def calculate_results(input):
    camel_cards = file_to_cards(input)
    # camel_cards = example_camel_cards
    # camel_cards = better_example

    hands, bids = parse_cards(camel_cards)
    ranks = rank_hands(hands)
    print_stats(ranks, hands, bids)

    total_winnings = sum([ranks[hand] * bid for hand, bid in zip(hands,bids)])    
    return total_winnings


if __name__ == "__main__":
    input = "input07.txt"
    output = calculate_results(input)

    print(f"Total winnings: {output}")