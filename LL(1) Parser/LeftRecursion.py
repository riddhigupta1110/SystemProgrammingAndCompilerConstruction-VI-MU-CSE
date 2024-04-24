def remove_left_recursion(dictionary):
    store = {}
    for lhs in dictionary:
        alpharules = []
        betarules = []
        allrhs = dictionary[lhs]
        for rhs in allrhs:
            if rhs[0] == lhs:
                alpharules.append(rhs[1:])
            else:
                betarules.append(rhs)
        if len(alpharules) > 0:
            lhs_ = lhs + "'"
            for beta in range(len(betarules)):
                betarules[beta].append(lhs_)
            dictionary[lhs] = betarules
            for alpha in range(len(alpharules)):
                alpharules[alpha].append(lhs_)
            alpharules.append('#')
            store[lhs_] = alpharules
    for rule in store:
        dictionary[rule] = store[rule]
    return dictionary


if __name__ == '__main__':
    dictionary = {}
    productions = []
    with open('LL(1) Parser/inputrecursion.txt', 'r') as input:
        productions = input.readlines()
        productions = [production.strip() for production in productions]

    for rule in productions:
        lhs, allrhs = rule.split('->')
        lhs = lhs.strip()
        multirhs = allrhs.split('|')
        multirhs = [multi.strip() for multi in multirhs]
        multirhs = [multi.split() for multi in multirhs]

        dictionary[lhs] = multirhs

    dictionary = remove_left_recursion(dictionary)

    for rule in dictionary:
        r = [''.join(_) for _ in dictionary[rule]]
        print(f"{rule} -> {' | '.join(r)}")