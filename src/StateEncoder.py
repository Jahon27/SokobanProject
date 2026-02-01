class StateEncoder:

    def encode_goal(self, step):
        self.theory.writeComment('Goal state - all boxes must be in targets')
        for box_id in range(len(self.map_data['boxes'])):
            self.theory.writeClause([self.predicates.reachedGoal(box_id + 1, step)])

    def encode_init_state(self):
        self.theory.writeComment('Initial state loaded from the map')

        # Targets on the map
        self.theory.writeComment('Targets on the map (fact)')
        for X, Y in self.coords:
            if (X, Y) in self.map_data['goals']:
                self.theory.writeClause([self.predicates.goal(X, Y)])
            else:
                self.theory.writeClause([self.predicates.negation(self.predicates.goal(X, Y))])

        # Initial position of the player
        self.theory.writeComment('Initial position of the player loaded from the map')
        for X, Y in self.coords:
            if (X, Y) == self.map_data['sokoban']:
                self.theory.writeClause([self.predicates.playerAt(X, Y, 0)])
            else:
                self.theory.writeClause([self.predicates.negation(self.predicates.playerAt(X, Y, 0))])

        # Initial boxes position
        self.theory.writeComment('Initial boxes position loaded from the map')
        for X, Y in self.coords:
            for index, box in enumerate(self.map_data['boxes']):
                if (X, Y) == box:
                    self.theory.writeClause([self.predicates.boxAt(index + 1, X, Y, 0)])
                else:
                    self.theory.writeClause([self.predicates.negation(self.predicates.boxAt(index + 1, X, Y, 0))])

        # Boxes in the target
        self.theory.writeComment('Boxes in the target')
        for index, box in enumerate(self.map_data['boxes']):
            if box in self.map_data['goals']:
                self.theory.writeClause([self.predicates.reachedGoal(index + 1, 0)])
            else:
                self.theory.writeClause([self.predicates.negation(self.predicates.reachedGoal(index + 1, 0))])

        # Initial empty squares
        self.theory.writeComment('Initial empty squares loaded from the map')
        for X, Y in self.coords:
            if (X, Y) not in self.map_data['boxes'] and (X, Y) != self.map_data['sokoban']:
                self.theory.writeClause([self.predicates.emptyCell(X, Y, 0)])
            else:
                self.theory.writeClause([self.predicates.negation(self.predicates.emptyCell(X, Y, 0))])