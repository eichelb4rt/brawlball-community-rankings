import math


INPUT_FILE = "rankings.txt"
OUTPUT_FILE = "results.txt"
LIST_SIZE = 4

LIST_POINTS = [5, 4, 3, 2, 1]
MENTION_POINTS = 0.5


# class TopFive:

def count_lists(lines: list[str]) -> int:
    if len(lines) == 0 or len(lines) == 1:
        return 0
    return math.ceil(len(lines) / LIST_SIZE)


def sanitize(name: str) -> str:
    return name.strip().lower()


def read_mentions(lines: list[str], n: int):
    """Reads nth rating list from the file lines."""

    line_idx = LIST_SIZE * n + 2
    if lines[line_idx].strip() == "-":
        return []

    mentions = lines[line_idx].split(',')
    return [sanitize(name) for name in mentions]


def read_top_five(lines: list[str], n: int):
    """Reads nth rating list from the file lines."""

    line_idx = LIST_SIZE * n + 1
    top_five = lines[line_idx].split(',')

    if len(top_five) != 5:
        print(f"Error in line {line_idx}: Top 5 should contain 5 names.")

    return [sanitize(name) for name in top_five]


def give_points(top_fives, mentions):
    """Generates points for all the people in the top five and mentions"""

    score = {}
    for top_five in top_fives:
        for name, points in zip(top_five, LIST_POINTS):
            if name not in score:
                score[name] = 0
            score[name] += points

    for mention_list in mentions:
        for mention in mention_list:
            if mention not in score:
                score[mention] = 0
            score[mention] += MENTION_POINTS
    return score


def gen_rank_string(points):
    points = sorted(points.items(), key=lambda item: item[1])
    points.reverse()
    rank_string = ""
    for i, (name, score) in enumerate(points):
        if i == 0 or score != last_score:
            current_rank = i + 1
        rank_string += f"{current_rank}. {name} ({score} points)\n"
        last_score = score
    return rank_string


def main():
    with open(INPUT_FILE, 'r') as f:
        lines = f.readlines()

    n_lists = count_lists(lines)
    top_fives = [read_top_five(lines, i) for i in range(n_lists)]
    mentions = [read_mentions(lines, i) for i in range(n_lists)]
    points = give_points(top_fives, mentions)
    result = gen_rank_string(points)
    print(result)
    with open(OUTPUT_FILE, 'w') as f:
        f.write(result)
    print(f"{OUTPUT_FILE} was updated.")


if __name__ == "__main__":
    main()
