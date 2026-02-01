# Sokoban SAT Solver - README

1. Vocabulary and Predicates

### State Predicates
- empty(X, Y, N)` - Square (X,Y) is empty at time step N
- playerAt(X, Y, N)` - Player is at position (X,Y) at time step N
- boxAt(boxID, X, Y, N)` - Box with ID BOX_ID is at position (X,Y) at time step N
- goal(X, Y)` - Position (X,Y) is a goal/target cell (static)
- reachedGoal(boxID, N)` - Box BOX_ID is in a goal at time step N

### Action Predicates
- move(fromX, fromY, toX, toY, N)` - Player moves from (fromX,fromY) to (toX,toY) at step N
- push(boxID, playerX, playerY, fromX, fromY, toX, toY, N)` - Push box BOX_ID from (fromX,fromY) to (toX,toY) with player at (playerX,playerY)
- `pushToGoal(boxID, playerX, playerY, fromX, fromY, toX, toY, N)` - Push box boxID to goal (toX,toY) from (fromX,fromY)

### Logical Rules
1. **Existence**: On each square there can be either a player, empty, or a box
2. **Exclusivity**: 
   - A box at one position cannot be at another position
   - Player at one position cannot be at another position
   - Maximum one entity per square (player, empty, or box)
3. **Actions**: At least one action per step, no two actions simultaneously
4. **Frame Axioms**: Entities not involved in actions persist unchanged

2. Installation and Dependencies

### Prerequisites
- Python 3.6+ (Developed with Python 3.13)
- MiniSat SAT Solver (included in `minisat/` directory)

# No external libraries required beyond Python standard library

3. Basic Usage
- To run the project, navigate to the root and execute the following command:
  `python main.py maps/map4.txt [limit]`

- TO run with User-friendly Interface
   `python main.py --gui`

4. Output Files
The solver generates several output files in the output/ directory:
- cnf.txt - CNF theory in human-readable format
- dimacs.txt - DIMACS format for MiniSat
- variables.txt - Variable mapping for predicates
- solution.txt - MiniSat solution output

5. Output Example and explaination
### When you run the solver, you'll see output like this:
```Writing theory and solving the problem...
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
pushToGoal(2,1,3,1,2,1,1,13)```

**Most importantly**, after the files are created, the program displays the step-by-step solution:

- Each line is one action the player must take
- Actions are numbered sequentially (1, 2, 3...)
- `move(x1,y1,x2,y2,N)` means: at step N, move from (x1,y1) to (x2,y2)
- `push(box,X,Y,x1,y1,x2,y2,N)` means: at step N, push box from (x1,y1) to (x2,y2) with player at (X,Y)
- `pushToGoal` is like push, but the box ends up in a goal position
