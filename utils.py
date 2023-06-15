import enum

from consts import TERMINAL_MOVE
from consts import SAFE_TILE, HAZARD_TILE


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


def convert_offset_to_move(offset: tuple[int, int]) -> Moves:
    if offset == (0, 1):
        return Moves.UP
    elif offset == (0, -1):
        return Moves.DOWN
    elif offset == (-1, 0):
        return Moves.LEFT
    elif offset == (1, 0):
        return Moves.RIGHT


def get_best_move(moves_dict: dict) -> Moves:
    best_move = Moves.UP
    best_value = moves_dict[best_move]
    for move in Moves:
        if best_value < moves_dict[move]:
            best_move = move
            best_value = moves_dict[move]

    return best_move


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


def avoid_snake(safe_moves: set, my_pos, snake):
    for move in safe_moves.copy():
        new_pos = apply_move_to_pos(my_pos, move)

        for body_pos in snake["body"]:
            if new_pos == body_pos:
                safe_moves[move] -= TERMINAL_MOVE


def generate_obstacle_board(game_state: dict) -> list[list[int]]:
    board_width = game_state["board"]["width"]
    board_height = game_state["board"]["height"]

    board = [[SAFE_TILE * board_width] for _ in range(board_height)]

    snakes = game_state["board"]["snakes"]

    for snake in snakes:
        snake_body = snake["body"]

        for body in snake_body:
            x = body["x"]
            y = body["y"]

            board[y][x] = HAZARD_TILE

    # TODO: take into account hazards as well in the future
    return board

