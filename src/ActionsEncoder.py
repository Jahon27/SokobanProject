class ActionsEncoder:
    def actions(self, step):
        self.action_move(step)
        self.action_push(step)
        self.action_pushToGoal(step)
        actions = []

        for fromX, fromY in self.coords:
            for toX, toY in self.coords:
                if self.is_adjacent((fromX, fromY), (toX, toY)):
                    actions.append(self.predicates.move(fromX, fromY, toX, toY, step))

        for box_id in range(len(self.map_data['boxes'])):
            for playerX, playerY in self.coords:
                for fromX, fromY in self.coords:
                    for toX, toY in self.coords:
                        if self.is_inline((playerX, playerY), (fromX, fromY), (toX, toY)):
                            actions.append(self.predicates.push(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step))
                            actions.append(self.predicates.pushToGoal(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step))

        self.theory.writeComment('At least one action happens')
        self.theory.writeClause(actions)
        self.theory.writeComment('Actions exclusivity')
        for action1 in range(len(actions)):
            for action2 in range(action1 + 1, len(actions)):
                if action1 != action2:
                    self.theory.writeClause(
                        [self.predicates.negation(actions[action1]), self.predicates.negation(actions[action2])])
        self.frame_problem(step)

    def action_move(self, step):
        self.theory.writeComment('Action move(fromX, fromY, toX, toY, step)')
        for fromX, fromY in self.coords:
            for toX, toY in self.coords:
                if self.is_adjacent((fromX, fromY), (toX, toY)):
                    # P+ conditions
                    self.theory.writeClause([self.predicates.negation(self.predicates.move(fromX, fromY, toX, toY, step)),self.predicates.playerAt(fromX, fromY, step - 1)])
                    self.theory.writeClause([self.predicates.negation(self.predicates.move(fromX, fromY, toX, toY, step)),self.predicates.emptyCell(toX, toY, step - 1)])
                    self.theory.writeClause([self.predicates.negation(self.predicates.move(fromX, fromY, toX, toY, step)),self.predicates.playerAt(toX, toY, step)])
                    self.theory.writeClause([self.predicates.negation(self.predicates.move(fromX, fromY, toX, toY, step)),self.predicates.emptyCell(fromX, fromY, step)])

    def action_push(self, step):
        self.theory.writeComment('Action push(boxID, playerX, playerY, fromX, fromY, toX, toY, step)')
        for box_id in range(len(self.map_data['boxes'])):
            for playerX, playerY in self.coords:
                for fromX, fromY in self.coords:
                    for toX, toY in self.coords:
                        if self.is_inline((playerX, playerY), (fromX, fromY), (toX, toY)):
                            self.theory.writeClause([self.predicates.negation(self.predicates.push(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step)), self.predicates.emptyCell(toX, toY, step - 1)])
                            self.theory.writeClause([self.predicates.negation(self.predicates.push(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step)), self.predicates.playerAt(playerX, playerY, step - 1)])
                            self.theory.writeClause([self.predicates.negation(self.predicates.push(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step)), self.predicates.boxAt(box_id + 1, fromX, fromY, step - 1)])
                            self.theory.writeClause([self.predicates.negation(self.predicates.push(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step)), self.predicates.negation(self.predicates.goal(toX, toY))])
                            self.theory.writeClause([self.predicates.negation(self.predicates.push(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step)), self.predicates.playerAt(fromX, fromY, step)])
                            self.theory.writeClause([self.predicates.negation(self.predicates.push(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step)), self.predicates.boxAt(box_id + 1, toX, toY, step)])
                            self.theory.writeClause([self.predicates.negation(self.predicates.push(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step)), self.predicates.emptyCell(playerX, playerY, step)])
                            self.theory.writeClause([self.predicates.negation(self.predicates.push(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step)), self.predicates.negation(self.predicates.reachedGoal(box_id + 1, step))])

    def action_pushToGoal(self, step):
        self.theory.writeComment('Action pushToGoal(boxID, playerX, playerY, fromX, fromY, toX, toY, step)')
        for box_id in range(len(self.map_data['boxes'])):
            for playerX, playerY in self.coords:
                for fromX, fromY in self.coords:
                    for toX, toY in self.coords:
                        if self.is_inline((playerX, playerY), (fromX, fromY), (toX, toY)):
                            self.theory.writeClause([self.predicates.negation(self.predicates.pushToGoal(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step)), self.predicates.emptyCell(toX, toY, step - 1)])
                            self.theory.writeClause([self.predicates.negation(self.predicates.pushToGoal(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step)), self.predicates.playerAt(playerX, playerY, step - 1)])
                            self.theory.writeClause([self.predicates.negation(self.predicates.pushToGoal(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step)), self.predicates.boxAt(box_id + 1, fromX, fromY, step - 1)])
                            self.theory.writeClause([self.predicates.negation(self.predicates.pushToGoal(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step)), self.predicates.goal(toX, toY)])
                            self.theory.writeClause([self.predicates.negation(self.predicates.pushToGoal(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step)), self.predicates.negation(self.predicates.reachedGoal(box_id + 1, step - 1))])
                            self.theory.writeClause([self.predicates.negation(self.predicates.pushToGoal(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step)), self.predicates.playerAt(fromX, fromY, step)])
                            self.theory.writeClause([self.predicates.negation(self.predicates.pushToGoal(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step)), self.predicates.boxAt(box_id + 1, toX, toY, step)])
                            self.theory.writeClause([self.predicates.negation(self.predicates.pushToGoal(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step)), self.predicates.emptyCell(playerX, playerY, step)])
                            self.theory.writeClause([self.predicates.negation(self.predicates.pushToGoal(box_id + 1, playerX, playerY, fromX, fromY, toX, toY, step)), self.predicates.reachedGoal(box_id + 1, step)])

    def frame_problem(self, step):
        self.theory.writeComment('Frame problem rules for step {}'.format(step))
        self.theory.writeComment('Frame 1 & 2: If player moves, box positions and target status remain unchanged')
        for box_id in range(len(self.map_data['boxes'])):
            for boxX, boxY in self.coords:
                for fromX, fromY in self.coords:
                    for toX, toY in self.coords:
                        if self.is_adjacent((fromX, fromY), (toX, toY)):
                            self.theory.writeClause([self.predicates.negation(self.predicates.boxAt(box_id + 1, boxX, boxY, step - 1)), self.predicates.negation(self.predicates.move(fromX, fromY, toX, toY, step)),self.predicates.boxAt(box_id + 1, boxX, boxY, step)])
                            self.theory.writeClause([self.predicates.boxAt(box_id + 1, boxX, boxY, step - 1), self.predicates.negation(self.predicates.move(fromX, fromY, toX, toY, step)), self.predicates.negation(self.predicates.boxAt(box_id + 1, boxX, boxY, step))])
                            self.theory.writeClause([self.predicates.negation(self.predicates.reachedGoal(box_id + 1, step - 1)), self.predicates.negation(self.predicates.move(fromX, fromY, toX, toY, step)), self.predicates.reachedGoal(box_id + 1, step)])
                            self.theory.writeClause([self.predicates.reachedGoal(box_id + 1, step - 1), self.predicates.negation(self.predicates.move(fromX, fromY, toX, toY, step)), self.predicates.negation(self.predicates.reachedGoal(box_id + 1, step))])
        self.theory.writeComment('Frame 3 & 4: If a box moves, other boxes remain unchanged')
        for box_id in range(len(self.map_data['boxes'])):
            for boxX, boxY in self.coords:
                for box_id2 in range(len(self.map_data['boxes'])):
                    if box_id != box_id2:
                        for playerX, playerY in self.coords:
                            for fromX, fromY in self.coords:
                                for toX, toY in self.coords:
                                    if self.is_inline((playerX, playerY), (fromX, fromY), (toX, toY)):
                                        self.theory.writeClause([self.predicates.negation(self.predicates.boxAt(box_id + 1, boxX, boxY, step - 1)), self.predicates.negation(self.predicates.push(box_id2 + 1, playerX, playerY, fromX, fromY, toX,toY, step)), self.predicates.boxAt(box_id + 1, boxX, boxY, step)])
                                        self.theory.writeClause([self.predicates.boxAt(box_id + 1, boxX, boxY, step - 1), self.predicates.negation(self.predicates.push(box_id2 + 1, playerX, playerY, fromX, fromY, toX,toY, step)), self.predicates.negation(self.predicates.boxAt(box_id + 1, boxX, boxY, step))])
                                        self.theory.writeClause([self.predicates.negation(self.predicates.boxAt(box_id + 1, boxX, boxY, step - 1)), self.predicates.negation(self.predicates.pushToGoal(box_id2 + 1, playerX, playerY, fromX, fromY, toX,toY, step)), self.predicates.boxAt(box_id + 1, boxX, boxY, step)])
                                        self.theory.writeClause([self.predicates.boxAt(box_id + 1, boxX, boxY, step - 1), self.predicates.negation(self.predicates.pushToGoal(box_id2 + 1, playerX, playerY, fromX, fromY, toX,toY, step)), self.predicates.negation(self.predicates.boxAt(box_id + 1, boxX, boxY, step))])
                                        self.theory.writeClause([self.predicates.negation(self.predicates.reachedGoal(box_id + 1, step - 1)), self.predicates.negation(self.predicates.push(box_id2 + 1, playerX, playerY, fromX, fromY, toX,toY, step)), self.predicates.reachedGoal(box_id + 1, step)])
                                        self.theory.writeClause([self.predicates.reachedGoal(box_id + 1, step - 1), self.predicates.negation(self.predicates.push(box_id2 + 1, playerX, playerY, fromX, fromY, toX, toY, step)), self.predicates.negation(self.predicates.reachedGoal(box_id + 1, step))])
                                        self.theory.writeClause([self.predicates.negation(self.predicates.reachedGoal(box_id + 1, step - 1)), self.predicates.negation(self.predicates.pushToGoal(box_id2 + 1, playerX, playerY, fromX, fromY, toX,toY, step)), self.predicates.reachedGoal(box_id + 1, step)])
                                        self.theory.writeClause([self.predicates.reachedGoal(box_id + 1, step - 1), self.predicates.negation(self.predicates.pushToGoal(box_id2 + 1, playerX, playerY, fromX, fromY, toX,toY, step)), self.predicates.negation(self.predicates.reachedGoal(box_id + 1, step))])