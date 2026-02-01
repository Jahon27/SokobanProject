import sys
from src.solver_factory import create_solver
from vis.gui import SokobanGUI

def main():
    # ---------- GUI MODE ----------
    if len(sys.argv) == 2 and sys.argv[1] == "--gui":
        gui = SokobanGUI()
        gui.run()
        return

    # ---------- CLI MODE ----------
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py <map_file> [limit]   # CLI solver")
        print("  python main.py --gui                # GUI mode")
        sys.exit(1)

    map_file = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20

    solver = create_solver(map_file, limit)
    solver.solve()

if __name__ == "__main__":
    main()
