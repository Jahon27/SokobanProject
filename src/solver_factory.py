from src.SokobanGameSolver import SokobanSolver
from src.MapLoader import MapLoader
from src.Helper import GeometryHelper
from src.ExclusivityEncoder import ExclusivityEncoder
from src.ActionsEncoder import ActionsEncoder
from src.StateEncoder import StateEncoder

def create_solver(map_file: str, limit: int = 80) -> SokobanSolver:
    ss = SokobanSolver(map_file)
    ss.set_limit(limit)
    ss.DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Map / geometry
    ss.load_map = MapLoader.load_map.__get__(ss)
    ss.generate_coords = MapLoader.generate_coords.__get__(ss)
    ss.is_inline = GeometryHelper.is_inline.__get__(ss)
    ss.is_adjacent = GeometryHelper.is_adjacent.__get__(ss)

    # exclusivity
    ss.box_exclusivity = ExclusivityEncoder.box_exclusivity.__get__(ss)
    ss.player_exclusivity = ExclusivityEncoder.player_exclusivity.__get__(ss)
    ss.position_exclusivity = ExclusivityEncoder.position_exclusivity.__get__(ss)
    ss.write_pairwise_exclusivity = ExclusivityEncoder.write_pairwise_exclusivity.__get__(ss)

    # actions / frame
    ss.actions = ActionsEncoder.actions.__get__(ss)
    ss.action_move = ActionsEncoder.action_move.__get__(ss)
    ss.action_push = ActionsEncoder.action_push.__get__(ss)
    ss.action_pushToGoal = ActionsEncoder.action_pushToGoal.__get__(ss)
    ss.frame_problem = ActionsEncoder.frame_problem.__get__(ss)

    # init + goal
    ss.encode_goal = StateEncoder.encode_goal.__get__(ss)
    ss.encode_init_state = StateEncoder.encode_init_state.__get__(ss)

    return ss
