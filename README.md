# Sokoban SAT Solver

This project solves the classical *Sokoban* puzzle by modeling it as a deterministic planning problem and encoding it into propositional satisfiability (SAT).

The goal is to automatically find a shortest sequence of actions that moves all crates onto goal cells.
The planning problem is solved using the MiniSat SAT solver, and the resulting plan can be visualized step by step using a graphical user interface.

The project was developed as part of the course *Computational Logic* at Comenius University in Bratislava.

---

## Project Overview

Sokoban is a single-agent puzzle game played on a two-dimensional grid consisting of walls, empty cells, movable crates, and goal cells.
The player can move in four directions and push crates, but cannot pull them or move through walls.

In this project, Sokoban is formulated as a classical planning problem:
- **States** represent the positions of the player and all crates at a given time step
- **Actions** describe valid moves and pushes
- **Goal condition** requires all crates to be placed on goal cells

The planning problem is encoded into conjunctive normal form (CNF) and solved incrementally using a SAT solver to obtain a shortest valid plan.

---

## Vocabulary and Predicates

### State Predicates

- `empty(X, Y, N)`
  Square `(X,Y)` is empty at time step `N`

- `playerAt(X, Y, N)`
  Player is at position `(X,Y)` at time step `N`

- `boxAt(boxID, X, Y, N)`
  Box with identifier `boxID` is at position `(X,Y)` at time step `N`

- `goal(X, Y)`
  Position `(X,Y)` is a goal (target) cell (static predicate)

- `reachedGoal(boxID, N)`
  Box `boxID` is located on a goal cell at time step `N`


### Action Predicates

- `move(fromX, fromY, toX, toY, N)`
  Player moves from `(fromX,fromY)` to `(toX,toY)` at step `N`

- `push(boxID, playerX, playerY, fromX, fromY, toX, toY, N)`
  Player pushes box `boxID` from `(fromX,fromY)` to `(toX,toY)` while standing at `(playerX,playerY)`

- `pushToGoal(boxID, playerX, playerY, fromX, fromY, toX, toY, N)`
  Push action in which box `boxID` is moved onto a goal cell


### Logical Rules

1. **Existence**
   Each square contains exactly one of the following: the player, a box, or is empty.

2. **Exclusivity**
   - A box cannot be located in more than one position at the same time
   - The player cannot occupy multiple positions simultaneously
   - At most one entity (player, empty, or box) may occupy a square

3. **Actions**
   - At least one action occurs at each time step
   - No two actions may occur simultaneously

4. **Frame Axioms**
   - Entities that are not affected by an action persist unchanged between consecutive time steps

---
### Output Files

The solver generates several output files in the `output/` directory:

- `cnf.txt` — CNF theory in human-readable format  
- `dimacs.txt` — DIMACS format for MiniSat  
- `variables.txt` — Variable mapping for predicates  
- `solution.txt` — MiniSat solution output  


### Output Example and Explanation

When you run the solver, you will see output similar to the following:

```text
Writing theory and solving the problem...
DONE
Solution found, actions:
pushToGoal(1,1,1,2,1,3,1,1)
move(2,1,1,1,2)
move(1,1,1,2,3)
move(1,2,1,3,4)
move(1,3,1,4,5)
move(1,4,2,4,6)
move(2,4,3,4,7)
move(3,4,3,3,8)
move(3,3,3,2,9)
push(2,3,2,2,2,1,2,10)
pushToGoal(3,2,2,2,3,2,4,11)
move(2,3,1,3,12)
pushToGoal(2,1,3,1,2,1,1,13)
```

**Most importantly**, after the files are created, the program displays the step-by-step solution:

- Each line is one action the player must take
- Actions are numbered sequentially (1, 2, 3...)
- `move(x1,y1,x2,y2,N)` means: at step N, move from (x1,y1) to (x2,y2)
- `push(box,X,Y,x1,y1,x2,y2,N)` means: at step N, push box from (x1,y1) to (x2,y2) with player at (X,Y)
- `pushToGoal` is like push, but the box ends up in a goal position


## Project Structure

```
SokobanProject/
│
├── src/              # Solver, encoders, predicates
├── theoryMaker/      # CNF writer and DIMACS translator
├── maps/             # Sokoban map files
├── vis/              # GUI and simulator
│   └── assets/       # Sprite images
├── minisat/          # MiniSat executable (Windows)
├── output/           # Generated CNF/DIMACS/solutions
├── main.py
├── requirements.txt
└── README.md
```
---
## Installation

``` pip install -r requirements.txt ```

- Run the solver on a specific map without GUI:
``` python main.py maps/map4.txt 50 ```

- Run the GUI:
``` python main.py --gui ```

