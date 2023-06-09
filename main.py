import typing
from utils import Moves, convert_move_to_str, apply_move_to_pos
from utils import get_manhattan_distance, find_closest_pos_in_list


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
    print("GAME OVER\n")


# ------------- API
def move(game_state: typing.Dict) -> typing.Dict:
    safe_moves: set = {
        Moves.UP,
        Moves.DOWN,
        Moves.LEFT,
        Moves.RIGHT,
    }

    head_pos = game_state["you"]["body"][0]
    neck_pos = game_state["you"]["body"][1]

    if neck_pos["x"] < head_pos["x"]:
        safe_moves.discard(Moves.LEFT)
    elif neck_pos["x"] > head_pos["x"]:
        safe_moves.discard(Moves.RIGHT)
    elif neck_pos["y"] < head_pos["y"]:
        safe_moves.discard(Moves.DOWN)
    elif neck_pos["y"] > head_pos["y"]:
        safe_moves.discard(Moves.UP)

    # Stay in bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    for move in safe_moves.copy():
        new_pos = apply_move_to_pos(head_pos, move)

        if not (0 <= new_pos['x'] < board_width) or not (0 <= new_pos['y'] <
                                                         board_height):
            safe_moves.discard(move)

    # Avoid itself
    my_body = game_state['you']['body']
    for move in safe_moves.copy():
        new_pos = apply_move_to_pos(head_pos, move)

        for body_pos in my_body:
            if new_pos == body_pos:
                safe_moves.discard(move)

    # Avoid other snakes
    opponents = game_state['board']['snakes']
    for other_snake in opponents:
        for move in safe_moves.copy():
            new_pos = apply_move_to_pos(head_pos, move)

            for body_pos in other_snake["body"]:
                if new_pos == body_pos:
                    safe_moves.discard(move)

    # If no more safe moves, return down
    if len(safe_moves) == 0:
        print(
            f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Move towards food
    food = game_state['board']['food']
    closest = find_closest_pos_in_list(head_pos, food)

    remaining_moves = list(safe_moves)

    best_move = remaining_moves[0]
    closest_distance = get_manhattan_distance(
        apply_move_to_pos(head_pos, best_move), closest)

    for move in remaining_moves[1:]:
        new_pos = apply_move_to_pos(head_pos, move)
        new_distance = get_manhattan_distance(new_pos, closest)
        if new_distance < closest_distance:
            closest_distance = new_distance
            best_move = move

    next_move = convert_move_to_str(best_move)
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
