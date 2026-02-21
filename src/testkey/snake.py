import curses
import random
import time
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Sequence, Tuple

Point = Tuple[int, int]


class Direction(str, Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


DIR_DELTAS = {
    Direction.UP: (-1, 0),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
    Direction.RIGHT: (0, 1),
}

OPPOSITE = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}


@dataclass(frozen=True)
class SnakeConfig:
    width: int = 16
    height: int = 12
    tick_seconds: float = 0.12


@dataclass(frozen=True)
class SnakeState:
    snake: Tuple[Point, ...]
    direction: Direction
    food: Point
    score: int
    alive: bool


def _initial_snake(width: int, height: int) -> Tuple[Point, ...]:
    center_row = height // 2
    center_col = width // 2
    return ((center_row, center_col), (center_row, center_col - 1), (center_row, center_col - 2))


def place_food(width: int, height: int, snake: Sequence[Point], rng: random.Random) -> Point:
    occupied = set(snake)
    candidates: List[Point] = []
    for r in range(height):
        for c in range(width):
            point = (r, c)
            if point not in occupied:
                candidates.append(point)
    if not candidates:
        return snake[0]
    return candidates[rng.randrange(len(candidates))]


def make_initial_state(config: SnakeConfig, rng: Optional[random.Random] = None) -> SnakeState:
    if config.width < 4 or config.height < 4:
        raise ValueError("Snake grid must be at least 4x4")
    if rng is None:
        rng = random.Random(0)
    snake = _initial_snake(config.width, config.height)
    food = place_food(config.width, config.height, snake, rng)
    return SnakeState(
        snake=snake,
        direction=Direction.RIGHT,
        food=food,
        score=0,
        alive=True,
    )


def change_direction(current: Direction, requested: Direction) -> Direction:
    if requested == OPPOSITE[current]:
        return current
    return requested


def step(state: SnakeState, config: SnakeConfig, rng: random.Random) -> SnakeState:
    if not state.alive:
        return state

    dr, dc = DIR_DELTAS[state.direction]
    head_r, head_c = state.snake[0]
    next_head = (head_r + dr, head_c + dc)

    if next_head[0] < 0 or next_head[0] >= config.height or next_head[1] < 0 or next_head[1] >= config.width:
        return SnakeState(
            snake=state.snake,
            direction=state.direction,
            food=state.food,
            score=state.score,
            alive=False,
        )

    ate_food = next_head == state.food
    body_to_check = state.snake if ate_food else state.snake[:-1]
    if next_head in body_to_check:
        return SnakeState(
            snake=state.snake,
            direction=state.direction,
            food=state.food,
            score=state.score,
            alive=False,
        )

    if ate_food:
        new_snake = (next_head,) + state.snake
        new_score = state.score + 1
        new_food = place_food(config.width, config.height, new_snake, rng)
    else:
        new_snake = (next_head,) + state.snake[:-1]
        new_score = state.score
        new_food = state.food

    return SnakeState(
        snake=new_snake,
        direction=state.direction,
        food=new_food,
        score=new_score,
        alive=True,
    )


def _draw(stdscr: curses.window, config: SnakeConfig, state: SnakeState, paused: bool) -> None:
    stdscr.erase()
    status = "PAUSED" if paused else ("GAME OVER" if not state.alive else "RUNNING")
    stdscr.addstr(0, 0, f"Snake  Score: {state.score}  Status: {status}  Keys: arrows/WASD, r=restart, p=pause, q=quit")

    border_top = "+" + ("-" * config.width) + "+"
    stdscr.addstr(2, 0, border_top)
    body = set(state.snake[1:])
    for r in range(config.height):
        row_chars = []
        for c in range(config.width):
            point = (r, c)
            if point == state.snake[0]:
                row_chars.append("O")
            elif point in body:
                row_chars.append("o")
            elif point == state.food:
                row_chars.append("*")
            else:
                row_chars.append(" ")
        stdscr.addstr(3 + r, 0, "|" + "".join(row_chars) + "|")
    stdscr.addstr(3 + config.height, 0, border_top)
    stdscr.refresh()


def _key_to_direction(key: int) -> Optional[Direction]:
    mapping = {
        curses.KEY_UP: Direction.UP,
        curses.KEY_DOWN: Direction.DOWN,
        curses.KEY_LEFT: Direction.LEFT,
        curses.KEY_RIGHT: Direction.RIGHT,
        ord("w"): Direction.UP,
        ord("s"): Direction.DOWN,
        ord("a"): Direction.LEFT,
        ord("d"): Direction.RIGHT,
        ord("W"): Direction.UP,
        ord("S"): Direction.DOWN,
        ord("A"): Direction.LEFT,
        ord("D"): Direction.RIGHT,
    }
    return mapping.get(key)


def run_snake_game(config: Optional[SnakeConfig] = None) -> None:
    if config is None:
        config = SnakeConfig()
    rng = random.Random(0)

    def _game(stdscr: curses.window) -> None:
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.keypad(True)
        state = make_initial_state(config, rng)
        paused = False
        last_tick = time.monotonic()

        while True:
            key = stdscr.getch()
            if key != -1:
                direction = _key_to_direction(key)
                if direction is not None and state.alive and not paused:
                    new_direction = change_direction(state.direction, direction)
                    state = SnakeState(
                        snake=state.snake,
                        direction=new_direction,
                        food=state.food,
                        score=state.score,
                        alive=state.alive,
                    )
                elif key in (ord("r"), ord("R")):
                    state = make_initial_state(config, rng)
                    paused = False
                elif key in (ord("p"), ord("P")) and state.alive:
                    paused = not paused
                elif key in (ord("q"), ord("Q")):
                    break

            now = time.monotonic()
            if now - last_tick >= config.tick_seconds:
                last_tick = now
                if state.alive and not paused:
                    state = step(state, config, rng)

            _draw(stdscr, config, state, paused)
            time.sleep(0.01)

    curses.wrapper(_game)
