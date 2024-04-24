def calc_first(dictionary, terms, nonterms):
    first_grammar = {}
    for key in reversed(list(dictionary.keys())):
        rules = dictionary[key]
        firsts = set()
        for rule in rules:
            if rule[0] in terms:
                firsts.add(rule[0])
            elif rule[0] in nonterms:
                firsts.update(first_grammar[rule[0]])
        first_grammar[key] = firsts 
    return first_grammar

def calc_follow(dictionary, terms, nonterms, firsts):
    follow_grammar = {nont: set() for nont in nonterms}
    follow_grammar[nonterms[0]].add('$')
    updated = True
    while updated:
        updated = False
        for lhs, allrhs in dictionary.items():
            for rhs in allrhs:
                for i, symbol in enumerate(rhs):
                    if symbol in nonterms:
                        if i == len(rhs)-1:
                            if follow_grammar[symbol].update(follow_grammar[lhs]):
                                updated = True
                        else:
                            next_symbol = rhs[i+1]
                            first_of_next_symbol = firsts[next_symbol]
                            if '#' in first_of_next_symbol:
                                # for epsilon condition
                                if follow_grammar[symbol].update(follow_grammar[lhs]):
                                    updated = True
                                # for remaining firsts
                                if follow_grammar[symbol].update(set(first_of_next_symbol)-{'#'}):
                                    updated = True
                            else:
                                if follow_grammar[symbol].update(set(first_of_next_symbol)):
                                    updated = True
        if not updated:
            break   
    return follow_grammar

if __name__ == '__main__':
    productions = []
    grammar = []
    terms = []
    nonterms = []
    dictionary = {}
    with open('LL(1) Parser/firstInput.txt', 'r') as input:
        productions = input.readlines()
        productions = [p.strip() for p in productions]
    
    grammar = productions[:-2]
    terms = productions[-1].split()
    nonterms = productions[-2].split()
    for line in grammar:
        lhs, allrhs = line.split('->')
        lhs = lhs.strip()
        multirhs = allrhs.split('|')
        multirhs = [m.strip() for m in multirhs]
        multirhs = [m.split() for m in multirhs]
        dictionary[lhs] = multirhs

    firsts = calc_first(dictionary, terms, nonterms)
    follows = calc_follow(dictionary, terms, nonterms, firsts)
    
    print('Rules')
    for rule in dictionary:
        r = [''.join(_) for _ in dictionary[rule]]
        print(f"{rule} -> {' | '.join(r)}")
    print('\nFirst():')
    for rule in reversed(firsts):
        r = [''.join(_) for _ in firsts[rule]]
        print(f"{rule} -> {' , '.join(r)}")
    print('\nFollow():')
    for rule in follows:
        r = [''.join(_) for _ in follows[rule]]
        print(f"{rule} -> {' , '.join(r)}")