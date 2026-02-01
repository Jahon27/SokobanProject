import os
import re
import subprocess
from src.MapLoader import MapLoader
from theoryMaker.theoryWriter import TheoryWriter
import theoryMaker.text2dimacs
from src.Predicates import Predicates

class SokobanSolver(object):
    def __init__(self, map_name):
        # === базовая директория проекта ===
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        OUTPUT_DIR = os.path.join(BASE_DIR, "output")

        # гарантируем, что папка существует
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # === абсолютные пути ===
        self.minisatPath = os.path.join(BASE_DIR, "minisat", "win", "minisat.exe")
        self.cnfFilePath = os.path.join(OUTPUT_DIR, "cnf.txt")
        self.dimacsFilePath = os.path.join(OUTPUT_DIR, "dimacs.txt")
        self.variablesFilePath = os.path.join(OUTPUT_DIR, "variables.txt")
        self.satSolutionFilePath = os.path.join(OUTPUT_DIR, "solution.txt")

        self.map_name = map_name
        self.map_data = MapLoader().load_map(map_name)
        self.coords = MapLoader().generate_coords(self.map_data)
        self.theory = TheoryWriter(self.cnfFilePath)
        self.predicates = Predicates()

        # лимит
        self.LIMIT = 20

    def set_limit(self, limit):
        self.LIMIT = limit

    def solve(self):
        solution_found = False
        i = 1
        sol = []
        print('Writing theory and solving the problem...')
        while not solution_found and i <= self.LIMIT:
            self.encode(i)
            self.to_dimacs()
            self.run_minisat()
            solution_found, sol = self.process_sol()
            i += 1
        self.theory.close()
        print('DONE')
        if solution_found:
            print('Solution found, actions:')
            for j in sol:
                print(j)
        else:
            print('Solution not found. Limit of steps reached ({})'.format(self.LIMIT))

    def run_minisat(self):
        args = (self.minisatPath, self.dimacsFilePath, self.satSolutionFilePath)
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()

    def to_dimacs(self):
        theoryMaker.text2dimacs.translate(self.cnfFilePath, self.dimacsFilePath, self.variablesFilePath)

    def read_sat(self, sat_solution_path):
        with open(sat_solution_path) as f:
            sat_status = f.readline().strip()
            if sat_status == 'UNSAT':
                return False, []
            assignments_line = f.readline().strip()
            return True, assignments_line.split()

    def read_pred(self, variables_file_path):
        predicates = {}
        expected_var = 0
        with open(variables_file_path) as f:
            for line in f:
                line = line.strip()
                if expected_var == 0:
                    expected_var = int(line)
                else:
                    predicates[expected_var] = line
                    expected_var = 0
        return predicates

    def extract_moves(self, minisat_vars, predicates):
        result = []
        for v in minisat_vars:
            v_int = int(v)
            if v_int > 0:
                pred = predicates.get(v_int, 'null')
                if pred.startswith('move') or pred.startswith('push'):
                    result.append(pred)
        return result

    def process_sol(self):
        sat, minisat_vars = self.read_sat(self.satSolutionFilePath)
        if not sat:
            return False, []
        predicates = self.read_pred(self.variablesFilePath)
        moves = self.extract_moves(minisat_vars, predicates)
        return True, moves

    def encode(self, iteration):
        self.theory.new_iteration()
        self.theory.writeComment('Map: {}'.format(self.map_name))
        self.encode_goal(iteration)
        self.encode_init_state()
        for step in range(1, iteration + 1):
            self.theory.writeComment('RULES - STEP {}'.format(step))
            self.theory.writeComment('"There can be either a player or nothing or one of the boxes on one cell ')
            for X, Y in self.coords:
                clause = [self.predicates.emptyCell(X, Y, step), self.predicates.playerAt(X, Y, step)]
                for box_id in range(len(self.map_data['boxes'])):
                    clause.append(self.predicates.boxAt(box_id + 1, X, Y, step))
                self.theory.writeClause(clause)
            self.player_exclusivity(step)
            self.box_exclusivity(step)
            self.position_exclusivity(step)
            self.actions(step)

    def solve_and_return_plan(self) -> list[str]:
        """
        Возвращает план в формате:
        - 'U','D','L','R'  для MOVE
        - 'u','d','l','r'  для PUSH / PUSH TO GOAL
        """
        solution_found = False
        i = 1
        sol = []

        # важно: на каждую попытку длины i ты перезаписываешь output файлы
        # Debug-файлы у тебя остаются как есть (cnf/dimacs/solution/variables)

        while not solution_found and i <= self.LIMIT:
            self.encode(i)
            self.to_dimacs()
            self.run_minisat()
            solution_found, sol = self.process_sol()
            i += 1

        self.theory.close()

        if not solution_found:
            return []

        # sol сейчас выглядит как список строк:
        # ["move(....)", "push(...)", "pushToGoal(...)"]
        # Нам нужно: отсортировать по step и преобразовать в UDLR/udlr
        return self._predicates_to_actions(sol)

    def _predicates_to_actions(self, preds: list[str]) -> list[str]:
        """
        preds: list строк типа move(...), push(...), pushToGoal(...)
        Возвращает список действий по порядку шагов.
        """
        parsed = []
        for p in preds:
            p = p.strip()

            if p.startswith("move"):
                # move(fromX, fromY, toX, toY, step)
                nums = list(map(int, re.findall(r"-?\d+", p)))
                # ожидаем 5 чисел
                if len(nums) >= 5:
                    fromX, fromY, toX, toY, step = nums[0], nums[1], nums[2], nums[3], nums[4]
                    act = self._dir_from_delta(toX - fromX, toY - fromY, push=False)
                    parsed.append((step, act))

            elif p.startswith("pushToGoal") or p.startswith("push"):
                # push(boxID, playerX, playerY, fromX, fromY, toX, toY, step)
                nums = list(map(int, re.findall(r"-?\d+", p)))
                # ожидаем 8 чисел
                if len(nums) >= 8:
                    # boxID, playerX, playerY, fromX, fromY, toX, toY, step
                    fromX, fromY, toX, toY, step = nums[3], nums[4], nums[5], nums[6], nums[7]
                    act = self._dir_from_delta(toX - fromX, toY - fromY, push=True)
                    parsed.append((step, act))

        # сортируем по step и возвращаем только действия
        parsed.sort(key=lambda x: x[0])
        return [a for _, a in parsed]

    def _dir_from_delta(self, dx: int, dy: int, push: bool) -> str:
        """
        В твоих координатах MapLoader: (row, col) => (x, y)
        Значит:
          dx = +1 => вниз (D)
          dx = -1 => вверх (U)
          dy = +1 => вправо (R)
          dy = -1 => влево (L)
        push=True => lowercase
        """
        if dx == -1 and dy == 0:
            return "u" if push else "U"
        if dx == 1 and dy == 0:
            return "d" if push else "D"
        if dx == 0 and dy == -1:
            return "l" if push else "L"
        if dx == 0 and dy == 1:
            return "r" if push else "R"
        raise ValueError(f"Illegal delta: dx={dx}, dy={dy}")