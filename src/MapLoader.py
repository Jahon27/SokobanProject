class MapLoader:
    def __init__(self):
        self.map_data = {}

    def parse_cell(self, char, row, col):
        if char == '#':
            self.map_data['walls'].append((row, col))
        elif char == 'S':  # sokoban
            self.map_data['sokoban'] = (row, col)
        elif char == 'X':  # goal
            self.map_data['goals'].append((row, col))
        elif char in ('C', 'c'):  # box
            self.map_data['boxes'].append((row, col))
            if char == 'c':  # box already on goal
                self.map_data['goals'].append((row, col))
        elif char == 's':  # sokoban on goal
            self.map_data['sokoban'] = (row, col)
            self.map_data['goals'].append((row, col))

    def initialize_map_data(self):
        self.map_data = {
            'map_size': (0, 0),
            'walls': [],
            'sokoban': (),
            'boxes': [],
            'goals': []
        }

    def load_map(self, file_name):
        self.initialize_map_data()
        max_col = 0
        with open(file_name) as f:
            for row, line in enumerate(f):
                line = line.rstrip('\n')  # odstráni newline
                max_col = max(max_col, len(line))
                for col, char in enumerate(line):
                    self.parse_cell(char, row, col)
        self.map_data['map_size'] = (row + 1, max_col)
        return self.map_data

    def generate_coords(self, data):
        coords = []
        for x in range(data['map_size'][0]):
            for y in range(data['map_size'][1]):
                if (x, y) not in data['walls']:
                    coords.append((x, y))
        return coords