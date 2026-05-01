def negate(clause):
    return f"~({clause})"

def resolve(c1, c2):
    # simple resolution placeholder
    return set(c1).union(set(c2))

def resolution(kb, query):
    clauses = kb.get_clauses()

    clauses.append([negate(query)])

    new = set()

    for i in range(len(clauses)):
        for j in range(i+1, len(clauses)):
            resolvent = resolve(clauses[i], clauses[j])
            if not resolvent:
                return True
            new.add(tuple(resolvent))

    return False