import enum


class Moves(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()


def convert_move_to_str(move: Moves) -> str:
    if move == Moves.UP:
        return "up"
    elif move == Moves.DOWN:
        return "down"
    elif move == Moves.LEFT:
        return "left"
    elif move == Moves.RIGHT:
        return "right"


def convert_move_to_offset(move: Moves) -> tuple[int, int]:
    if move == Moves.UP:
        return (0, 1)
    elif move == Moves.DOWN:
        return (0, -1)
    elif move == Moves.LEFT:
        return (-1, 0)
    elif move == Moves.RIGHT:
        return (1, 0)


def apply_move_to_pos(current_pos, move: Moves) -> dict:
    offset = convert_move_to_offset(move)
    return {
        'x': current_pos['x'] + offset[0],
        'y': current_pos['y'] + offset[1]
    }


def get_manhattan_distance(pos_1, pos_2) -> int:
    return abs(pos_1['x'] - pos_2['x']) + abs(pos_1['y'] - pos_2['y'])


def find_closest_pos_in_list(current_pos, other_pos_list: list) -> dict:
    closest_pos = other_pos_list[0]
    closest_distance = get_manhattan_distance(current_pos, closest_pos)

    for other_pos in other_pos_list[1:]:
        distance = get_manhattan_distance(current_pos, other_pos)
        if distance < closest_distance:
            closest_pos = other_pos

    return closest_pos
