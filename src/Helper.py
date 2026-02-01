class GeometryHelper:
    def is_inline(self, playerXY, fromXY, toXY):
        if not self.is_adjacent(fromXY, toXY) or not self.is_adjacent(playerXY, fromXY) or playerXY == toXY:
            return False
        if fromXY[0] == toXY[0]:
            return fromXY[0] == playerXY[0]
        if fromXY[1] == toXY[1]:
            return fromXY[1] == playerXY[1]
        return False

    def is_adjacent(self, c1, c2):
        if c1 == c2:
            return False
        if c1[0] == c2[0] and c1[1] == c2[1] + 1:
            return True
        if c1[0] == c2[0] and c1[1] == c2[1] - 1:
            return True
        if c1[1] == c2[1] and c1[0] == c2[0] + 1:
            return True
        if c1[1] == c2[1] and c1[0] == c2[0] - 1:
            return True
        return False