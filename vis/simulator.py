from dataclasses import dataclass

DIRS = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}

@dataclass(frozen=True)
class State:
    player: tuple[int,int]
    boxes: frozenset[tuple[int,int]]

class SokobanSimulator:
    def __init__(self, walls:set[tuple[int,int]], goals:set[tuple[int,int]]):
        self.walls = walls
        self.goals = goals

    def is_free(self, cell, boxes):
        return cell not in self.walls and cell not in boxes

    def step(self, state: State, action: str) -> State:
        # action: 'U','D','L','R' move
        # action: 'u','d','l','r' push
        if action.upper() not in DIRS:
            raise ValueError(f"Unknown action {action}")

        dx, dy = DIRS[action.upper()]
        px, py = state.player
        next_cell = (px + dx, py + dy)

        boxes = set(state.boxes)

        if action.isupper():
            # MOVE: next must be free
            if not self.is_free(next_cell, boxes):
                raise ValueError("Illegal MOVE")
            return State(player=next_cell, boxes=frozenset(boxes))

        else:
            # PUSH: next must contain box, and cell after it must be free
            if next_cell not in boxes:
                raise ValueError("Illegal PUSH (no box)")
            beyond = (next_cell[0] + dx, next_cell[1] + dy)
            if not self.is_free(beyond, boxes):
                raise ValueError("Illegal PUSH (blocked)")
            boxes.remove(next_cell)
            boxes.add(beyond)
            return State(player=next_cell, boxes=frozenset(boxes))

    def is_goal(self, state: State) -> bool:
        return all(b in self.goals for b in state.boxes)
