class ExclusivityEncoder:
    def write_pairwise_exclusivity(self, items, clause_fn):
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                lit1, lit2 = clause_fn(items[i], items[j])
                self.theory.writeClause([self.predicates.negation(lit1),
                                         self.predicates.negation(lit2)])

    def box_exclusivity(self, step):
        self.theory.writeComment('Boxes: exclusivity of positions')
        for box_id in range(len(self.map_data['boxes'])):
            self.write_pairwise_exclusivity(self.coords, lambda c1, c2: (self.predicates.boxAt(box_id + 1, *c1, step), self.predicates.boxAt(box_id + 1, *c2, step)))

    def player_exclusivity(self, step):
        self.theory.writeComment('Player: exclusivity of positions')
        self.write_pairwise_exclusivity(self.coords, lambda c1, c2: (self.predicates.playerAt(*c1, step), self.predicates.playerAt(*c2, step)))

    def position_exclusivity(self, step):
        self.theory.writeComment('Square exclusivity: player / empty / box')
        for X, Y in self.coords:
            self.theory.writeClause([self.predicates.negation(self.predicates.playerAt(X, Y, step)), self.predicates.negation(self.predicates.emptyCell(X, Y, step))])
            # player vs each box, empty vs each box
            for box_id in range(len(self.map_data['boxes'])):
                box_lit = self.predicates.boxAt(box_id + 1, X, Y, step)
                self.theory.writeClause([self.predicates.negation(self.predicates.playerAt(X, Y, step)),self.predicates.negation(box_lit)])
                self.theory.writeClause([self.predicates.negation(self.predicates.emptyCell(X, Y, step)), self.predicates.negation(box_lit)])
