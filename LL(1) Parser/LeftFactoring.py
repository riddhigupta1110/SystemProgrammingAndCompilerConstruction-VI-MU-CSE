def remove_left_factoring(dictionary):
    def find_common_prefix(allrhs):
        if not allrhs:
            return []
        prefix = allrhs[0][0]
        for rhs in allrhs[1:]:
            if rhs[0][0] != prefix[0]:
                continue
            length = min(len(prefix), len(rhs[0]))
            i = 0
            while(i < length and prefix[i] == rhs[0][i]):
                i += 1
            prefix = prefix[:i]
        return prefix
    
    store = {}
    for lhs in dictionary:
        allrhs = dictionary[lhs]
        prefix = find_common_prefix(allrhs)
        present = []
        absent = []
        for rhs in allrhs:
            if prefix in rhs[0]:
                present.append(rhs[0])
            else:
                absent.append(rhs[0])
        if len(present) > 0:
            lhs_ = lhs + "'"
            newrhs = prefix + lhs_
            store[lhs] = [newrhs]
            for p in present:
                rhs = p.lstrip(prefix)
                if lhs_ in store.keys():
                    store[lhs_].append(rhs)
                else:
                    store[lhs_] = [rhs]
        if len(absent) > 0:
            store[lhs].extend([abs for abs in absent])
    return store

if __name__ == '__main__':
    grammar = 'A -> bE+acF | bE+F'
    dictionary = {}
    lhs, rhs = grammar.split('->')
    lhs = lhs.strip()
    multirhs = rhs.split('|')
    multirhs = [multi.strip() for multi in multirhs]
    print(multirhs)
    multirhs = [multi.split() for multi in multirhs]
    print(multirhs)
    dictionary[lhs] = multirhs

    dictionary = remove_left_factoring(dictionary)

    for rule in dictionary:
        r = [''.join(_) for _ in dictionary[rule]]
        print(f"{rule} -> {' | '.join(r)}")