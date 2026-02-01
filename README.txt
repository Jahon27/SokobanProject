SOKOBAN SAT SOLVER
=================

This project solves the classical Sokoban puzzle by modeling it as a SAT-based planning problem.
The game dynamics are encoded into propositional logic and solved using the MiniSat SAT solver.
A graphical user interface (GUI) is provided to visualize the computed plan step by step.


----------------------------------------------------------------
1. VOCABULARY AND PREDICATES
----------------------------------------------------------------

STATE PREDICATES

- empty(X, Y, N)
  Square (X,Y) is empty at time step N

- playerAt(X, Y, N)
  Player is at position (X,Y) at time step N

- boxAt(boxID, X, Y, N)
  Box with ID boxID is at position (X,Y) at time step N

- goal(X, Y)
  Position (X,Y) is a goal cell (static)

- reachedGoal(boxID, N)
  Box boxID is placed on a goal at time step N


ACTION PREDICATES

- move(fromX, fromY, toX, toY, N)
  Player moves from (fromX,fromY) to (toX,toY) at step N

- push(boxID, playerX, playerY, fromX, fromY, toX, toY, N)
  Player pushes box boxID from (fromX,fromY) to (toX,toY)

- pushToGoal(boxID, playerX, playerY, fromX, fromY, toX, toY, N)
  Same as push, but the box ends up in a goal cell


LOGICAL RULES

1. Existence
   Each cell contains exactly one of: player, a box, or is empty.

2. Exclusivity
   - A box cannot be in two positions simultaneously
   - The player cannot occupy multiple positions
   - At most one entity per cell

3. Actions
   - At least one action occurs at each time step
   - No two actions occur simultaneously

4. Frame Axioms
   - Entities not affected by an action persist unchanged


----------------------------------------------------------------
2. INSTALLATION AND DEPENDENCIES
----------------------------------------------------------------

PREREQUISITES

- Python 3.9 or newer (developed and tested with Python 3.13)
- MiniSat SAT solver
  - Windows: included in minisat/win/minisat.exe
  - Linux/macOS: install MiniSat separately and update solver path if needed
- Pygame (required only for GUI visualization)


INSTALL DEPENDENCIES

Run the following command in the project root:

    pip install -r requirements.txt


----------------------------------------------------------------
3. BASIC USAGE
----------------------------------------------------------------

COMMAND-LINE SOLVER

Run the solver on a specific map:

    python main.py maps/map4.txt [limit]

Example:

    python main.py maps/map4.txt 60


GRAPHICAL USER INTERFACE (GUI)

Run the graphical interface:

    python vis/gui.py

The GUI allows map selection, automatic solving, and step-by-step visualization
of the computed plan.


----------------------------------------------------------------
4. OUTPUT FILES
----------------------------------------------------------------

The solver generates the following files in the output/ directory:

- cnf.txt
  CNF theory in human-readable form

- dimacs.txt
  DIMACS CNF file for the MiniSat solver

- variables.txt
  Mapping between propositional variables and predicates

- solution.txt
  Raw output produced by MiniSat


----------------------------------------------------------------
5. OUTPUT EXAMPLE AND EXPLANATION
----------------------------------------------------------------

Example solver output:

    Writing theory and solving the problem...
    DONE
    Solution found, actions:
    pushToGoal(1,1,1,2,1,3,1,1)
    move(2,1,1,1,2)
    move(1,1,1,2,3)
    move(1,2,1,3,4)
    ...


INTERPRETATION

- Each line represents one action
- Actions are ordered by time step
- move(x1,y1,x2,y2,N)
  At step N, move from (x1,y1) to (x2,y2)

- push(boxID,X,Y,x1,y1,x2,y2,N)
  At step N, push a box from (x1,y1) to (x2,y2)

- pushToGoal
  Same as push, but the box reaches a goal cell

After a solution is found, the GUI visualizes the execution of the plan
by animating each action step by step.


----------------------------------------------------------------
6. PROJECT STRUCTURE
----------------------------------------------------------------

Project directory layout:

    .
    ├── src/            SAT solver, encoders, predicates
    ├── theoryMaker/    CNF writer and DIMACS translator
    ├── maps/           Sokoban map files
    ├── vis/            GUI and simulator
    │   └── assets/     Sprite images
    ├── minisat/        MiniSat executable (Windows)
    ├── output/         Generated CNF/DIMACS/solutions
    ├── main.py
    ├── requirements.txt
    └── README.txt


----------------------------------------------------------------
7. NOTES AND LIMITATIONS
----------------------------------------------------------------

- Larger maps may require higher plan limits and longer solving times
- SAT-based planning guarantees correctness but may be slow for complex levels
- The GUI is intended for visualization only, not for manual gameplay


----------------------------------------------------------------
8. AUTHOR
----------------------------------------------------------------

Jahonoro Tojieva  
Computational Logic Project
