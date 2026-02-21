import random

import pytest

from testkey.snake import (
    Direction,
    SnakeConfig,
    SnakeState,
    change_direction,
    make_initial_state,
    place_food,
    step,
)


def test_initial_state_defaults():
    config = SnakeConfig(width=10, height=8)
    state = make_initial_state(config, random.Random(0))
    assert state.direction == Direction.RIGHT
    assert state.score == 0
    assert state.alive is True
    assert len(state.snake) == 3
    assert state.food not in state.snake


def test_move_forward_without_food():
    config = SnakeConfig(width=8, height=8)
    state = SnakeState(
        snake=((3, 3), (3, 2), (3, 1)),
        direction=Direction.RIGHT,
        food=(0, 0),
        score=0,
        alive=True,
    )
    next_state = step(state, config, random.Random(0))
    assert next_state.snake == ((3, 4), (3, 3), (3, 2))
    assert next_state.score == 0
    assert next_state.food == (0, 0)
    assert next_state.alive is True


def test_change_direction_blocks_reverse():
    assert change_direction(Direction.RIGHT, Direction.LEFT) == Direction.RIGHT
    assert change_direction(Direction.UP, Direction.LEFT) == Direction.LEFT


def test_growth_and_score_on_food():
    config = SnakeConfig(width=8, height=8)
    state = SnakeState(
        snake=((2, 2), (2, 1), (2, 0)),
        direction=Direction.RIGHT,
        food=(2, 3),
        score=0,
        alive=True,
    )
    next_state = step(state, config, random.Random(1))
    assert next_state.snake == ((2, 3), (2, 2), (2, 1), (2, 0))
    assert next_state.score == 1
    assert next_state.food not in next_state.snake


def test_wall_collision_sets_game_over():
    config = SnakeConfig(width=5, height=5)
    state = SnakeState(
        snake=((0, 2), (1, 2), (2, 2)),
        direction=Direction.UP,
        food=(4, 4),
        score=1,
        alive=True,
    )
    next_state = step(state, config, random.Random(0))
    assert next_state.alive is False
    assert next_state.snake == state.snake
    assert next_state.score == 1


def test_self_collision_sets_game_over():
    config = SnakeConfig(width=8, height=8)
    state = SnakeState(
        snake=((2, 2), (2, 1), (3, 1), (3, 2), (3, 3), (2, 3)),
        direction=Direction.LEFT,
        food=(0, 0),
        score=2,
        alive=True,
    )
    next_state = step(state, config, random.Random(0))
    assert next_state.alive is False


def test_move_into_tail_is_allowed_when_not_eating():
    config = SnakeConfig(width=8, height=8)
    state = SnakeState(
        snake=((2, 2), (2, 1), (3, 1), (3, 2)),
        direction=Direction.DOWN,
        food=(0, 0),
        score=0,
        alive=True,
    )
    next_state = step(state, config, random.Random(0))
    assert next_state.alive is True
    assert next_state.snake == ((3, 2), (2, 2), (2, 1), (3, 1))
    assert next_state.score == 0


def test_place_food_returns_head_when_board_full():
    snake = (
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
    )
    food = place_food(2, 2, snake, random.Random(0))
    assert food == (0, 0)


def test_invalid_config_rejected():
    with pytest.raises(ValueError):
        make_initial_state(SnakeConfig(width=3, height=6), random.Random(0))
