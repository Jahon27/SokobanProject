class Predicates:
    @staticmethod
    def push(box_id, playerX, playerY, fromX, fromY, toX, toY, step):
        return 'push({},{},{},{},{},{},{},{})'.format(
            box_id, playerX, playerY, fromX, fromY, toX, toY, step)

    @staticmethod
    def pushToGoal(box_id, playerX, playerY, fromX, fromY, toX, toY, step):
        return 'pushToGoal({},{},{},{},{},{},{},{})'.format(
            box_id, playerX, playerY, fromX, fromY, toX, toY, step)

    @staticmethod
    def move(fromX, fromY, toX, toY, step):
        return 'move({},{},{},{},{})'.format(fromX, fromY, toX, toY, step)

    @staticmethod
    def emptyCell(X, Y, step):
        return 'emptyCell({},{},{})'.format(X, Y, step)

    @staticmethod
    def playerAt(X, Y, step):
        return 'playerAt({},{},{})'.format(X, Y, step)

    @staticmethod
    def boxAt(box_id, X, Y, step):
        return 'boxAt({},{},{},{})'.format(box_id, X, Y, step)

    @staticmethod
    def goal(X, Y):
        return 'goal({},{})'.format(X, Y)

    @staticmethod
    def reachedGoal(box_id, step):
        return 'reachedGoal({},{})'.format(box_id, step)

    @staticmethod
    def negation(predicate):
        return '-' + predicate