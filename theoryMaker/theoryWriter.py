class TheoryWriter(object):
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'w')

    def new_iteration(self):
        if not self.closed():
            self.file.close()
        self.file = open(self.filename, 'w')

    def writeLiteral(self, lit):
        self.file.write('{} '.format(lit))

    def finishClause(self):
        self.file.write('\n')
        self.file.flush()

    def writeClause(self, clause):
        for l in clause:
            self.writeLiteral(l)
        self.finishClause()

    def writeImpl(self, left, right):
        self.writeClause(['-' + left, right])

    def writeComment(self, comment):
        for line in comment.split('\n'):
            self.file.write('c {}\n'.format(line))

    def closed(self):
        return self.file.closed

    def close(self):
        self.file.close()
