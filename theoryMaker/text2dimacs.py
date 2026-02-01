class Vars(dict):
    def maxVar(self):
        import functools
        return functools.reduce(max, self.values(), 0)
    def __missing__(self, key):
        val = self.maxVar() + 1
        self[key] = val
        return val

def translate(inf, outf, varsf):
    clauses = []
    varMap = Vars()
    with open(inf,'r') as f: 
        for line in f:
            clause = []
            tokens = line.split()
            if len(tokens) == 0 or tokens[0] == 'c':
                continue
            for w in line.split():
                if w in ['∨', 'v']:
                    continue
                neg  = w[0] in ['¬', '-']
                if neg:
                    w = w[1:]
                clause.append(varMap[w] * (-1 if neg else 1))
            clauses.append((line,clause))

    with open(outf,'w') as f:
        f.write('p cnf %d %d\n' % (varMap.maxVar(), len(clauses)))
        for line, clause in clauses:
            f.write('c %s' % line)
            f.write('%s 0\n' % ' '.join([str(x) for x in clause]))

    with open(varsf, 'w') as f:
        for num, var in sorted([(num,var) for var,num in varMap.items()]):
            f.write('%d\n%s\n' % (num, var))
