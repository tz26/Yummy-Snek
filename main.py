import typing

from consts import TERMINAL_MOVE, POTENTIAL_HEAD, FOOD_DISTANCE_FACTOR

from utils import Moves, convert_move_to_str, apply_move_to_pos
from utils import get_best_move
from utils import get_manhattan_distance, find_closest_pos_in_list
from utils import avoid_snake


# ----------------- API
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "tz26",
        "color": "#888888",
        "head": "default",
        "tail": "default",
    }


# ------------------ API
def start(game_state: typing.Dict):
    print("GAME START")


# ------------------- API
def end(game_state: typing.Dict):
    print("GAME OVER")


# ------------- API
def move(game_state: typing.Dict) -> typing.Dict:
    moves_dict: dict = {
        Moves.UP: 0,
        Moves.DOWN: 0,
        Moves.LEFT: 0,
        Moves.RIGHT: 0,
    }

    snake = game_state["you"]
    head_pos = snake["body"][0]

    # Stay in bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    for move in moves_dict:
        new_pos = apply_move_to_pos(head_pos, move)

        if not (0 <= new_pos['x'] < board_width) or not (0 <= new_pos['y'] <
                                                         board_height):
            moves_dict[move] -= TERMINAL_MOVE

    # Avoid itself
    avoid_snake(moves_dict, head_pos, snake)

    # Avoid other snakes
    opponents = game_state['board']['snakes']
    for other_snake in opponents:
        if other_snake["id"] != snake["id"]:
            avoid_snake(moves_dict, head_pos, other_snake)
    
            other_snake_head_pos = other_snake["body"][0]
            for move in Moves:
                new_other_head_pos = apply_move_to_pos(other_snake_head_pos, move)

                for safe_move in moves_dict.copy():
                    new_pos = apply_move_to_pos(head_pos, safe_move)
                    if new_pos == new_other_head_pos:
                        moves_dict[move] -= POTENTIAL_HEAD

    # # If no more safe moves, return down
    # if len(safe_moves) == 0:
    #     print(
    #         f"MOVE {game_state['turn']}: No safe moves detected! Moving straight")
    #     neck_pos = snake["body"][1]
        
    #     offset = head_pos[0] - neck_pos[0], head_pos[1] - neck_pos[1]
    #     move = convert_offset_to_move(offset)
    #     move = convert_move_to_str(move)
    #     return {"move": move}

    # Move towards food
    food = game_state['board']['food']
    closest_food = find_closest_pos_in_list(head_pos, food)

    for move in Moves:
        new_pos = apply_move_to_pos(head_pos, move)
        distance = get_manhattan_distance(new_pos, closest_food)

        moves_dict[move] -= distance / FOOD_DISTANCE_FACTOR
    
    best_move = get_best_move(moves_dict)

    next_move = convert_move_to_str(best_move)
    print(f"MOVE {game_state['turn']}: {next_move}")
    print(f"{moves_dict=}")
    return {"move": next_move}


if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
