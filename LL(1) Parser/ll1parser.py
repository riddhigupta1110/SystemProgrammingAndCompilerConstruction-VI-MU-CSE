#LL1 parser
#1. Left Factoring
#2. left recursion
#3. First
#4. Follow

import re,os

epsilon = '\u03B5'

def printFF(first,follow,rules):
    rowFormat = '{:<1} {:<3} {:<2} {:<10} {:<1} {:<15} {:<1} {:<15} {:<1}'
    for lhs,rhs in rules.items():
        Fstring = '{'
        for i in first[lhs]:
            Fstring = Fstring + i + ","
        F1string = '{'
        for i in follow[lhs]:
            F1string = F1string + i + ","
        Rstring = ''
        for i in rules[lhs]:
            Rstring = Rstring + i + " / "
        print(rowFormat.format('|',lhs,'->',Rstring[:-2],'|',Fstring[:-1]+'}','|',F1string[:-1]+'}','|',))
    

def printRules(rules):
    rowFormat = '{:<1} {:<3} {:<3} {:<10} {:<1}'
    for lhs,rhs in rules.items():
        rString = ''
        for r in rhs:
            rString = rString + r + " / "
        print('-'*22)
        print(rowFormat.format('|',lhs,'->',rString[:-2],'|'))
    print('-'*22)

def readFile(fileName):
    rules = {}
    with open(fileName,'r') as file:
        fileContent = file.read().split('\n')
    for line in fileContent:
        lhs,rhs = line.split('->')
        rules[lhs] = rhs.split("|")
        print(rhs.split("|"))

    for lhs,rhs in rules.items():
        for index,i in enumerate(rhs):
            if i == "#":
                rules[lhs][index] = epsilon
            else:
                idx = i.find('#')
                print(i,idx)
                if idx != -1:
                    print(rules[lhs][index])
                    rules[lhs][index] = rules[lhs][index][:idx]+epsilon+rules[lhs][index][idx+1:]

    return rules

def LeftRecursion(rules):
    lr = []
    for lhs,rhs in rules.items():
        if lhs == rhs[0][0]:
            lr.append(lhs)

    if len(lr) == 0:
        print('There is no left recursion')
        return rules

    for lhs in lr:
        alpha = rules[lhs][0][1:]
        beta = rules[lhs][1:]

        rules[lhs] = [f"{b}{lhs}`" for b in beta]
        rules[f"{lhs}`"] = [f"{alpha[0]}{lhs}`",epsilon]

    return rules

def LeftFactoring(rules):
    lf = {}
    for lhs,rhs in rules.items():
        alpha = []
        for index,r in enumerate(rhs):
            if index == 0:
                continue
            temp = os.path.commonprefix([rhs[0],r])
            alpha = temp if len(temp) > len(alpha) else alpha

        if len(alpha) != 0:
            lf[lhs] = alpha

    if len(lf) == 0:
        print('There is no left Factoring')
        return rules

    for lhs,alpha in lf.items():
        beta = []
        gamma = []
        beta_pattern = re.compile(f"{re.escape(alpha)}(.*)")
        for rhs in rules[lhs]:
            match = re.match(beta_pattern,rhs)
            print(match)
            if match == None:
                gamma.append(rhs)
            else:
                beta.append(match.group(1))

        rules[lhs] = [f"{alpha}{lhs}`"]
        for i in gamma:
            rules[lhs].append(i)
        rules[f"{lhs}`"] = [i for i in beta]
    return rules

def maintainOrder(rules):
    newRules = {}
    for lhs,rhs in rules.items():
        if lhs not in newRules:
            newRules[lhs] = rhs
            if f"{lhs}`" in rules:
                newRules[f"{lhs}`"] = rules[f"{lhs}`"]
    return newRules

def FindFirst(rules):
    Tpattern = re.compile(r"[a-z]+|\+|\-|\*|\/|\(|\)|\{|\}|\[|\]")
    NTpattern = re.compile(f'[A-Z]`?')
    first = {}
    for lhs,rhs in reversed(rules.items()):
        first[lhs] = []
        for r in rhs:
            NTmatch = re.match(NTpattern,r)
            if NTmatch == None:
                Tmatch = Tpattern.match(r)
                if Tmatch == None:
                    first[lhs].append(epsilon)
                else:
                    first[lhs].append(Tmatch[0])
            else:
                for i in first[NTmatch[0]]:
                    first[lhs].append(i)
    return first

def FindFollow(rules):
    print(rules)
    Tpattern = re.compile(r"[a-z]+|\+|\-|\*|\/|\(|\)|\{|\}|\[|\]")
    NTpattern = re.compile(f'[A-Z]`?')
    follow = {}
    for LHS,rhs in rules.items():
        print(follow)
        if not follow:
            follow[LHS] = ['$']
        step = 0 if len(LHS) == 1 else 1
        valueRet = FollowProcess(LHS,rules)
        print(LHS,valueRet)
        if valueRet == None:
            continue
        if valueRet[0] == 'append':
            if LHS not in follow:
                follow[LHS] = []
            follow[LHS].append(valueRet[1])
        elif valueRet[0] == 'follow':
            if LHS not in follow:
                follow[LHS] = []
            for i in follow[valueRet[1]]:
                follow[LHS].append(i)
        else:
            if LHS not in follow:
                    follow[LHS] = []
            for i in first[valueRet[2]]:
                if i != epsilon:
                    follow[LHS].append(i)
                else:
                    ruleCopy = rules[valueRet[1]]
                    ruleCopy[0].replace(valueRet[2],"")
                    idx = ruleCopy[0].find(LHS)
                    try:
                        if idx+step+1 < len(ruleCopy):
                            if Tpattern.match(ruleCopy[0][idx+step+1]):
                                follow[LHS].append(ruleCopy[0][idx+step+1])
                            else:
                                var = ruleCopy[0][idx+step+1]
                                try:
                                    if ruleCopy[0][idx+step+2] == '`':
                                        var = f'{ruleCopy[0][idx+step+1]}`'
                                except:
                                    print()
                                for j in first[var]:
                                    follow[LHS].append(j)
                        else:
                            for i in follow[valueRet[1]]:
                                follow[LHS].append(i)
                    except:
                        print()
    return follow

def FollowProcess(LHS,rules):
    Tpattern = re.compile(r"[a-z]+|\+|\-|\*|\/|\(|\)|\{|\}|\[|\]")
    NTpattern = re.compile(f'[A-Z]`?')
    step = 0 if len(LHS) == 1 else 1
    for lhs,rhs in rules.items():
        if lhs == LHS:
            continue
        for rule in rhs:
            try:
                index = rule.find(LHS)
                if index == -1:
                    continue
            except:
                print()

            try:
                if len(LHS) == 1 and rule[index+1] == '`':
                    continue
            except:
                print()
            print(rule,index)
            if index+step == len(rule)-1:
                return ['follow',lhs]   
            elif index+step+1 < len(rule):
                Tmatch = Tpattern.match(rule[index+step+1])
                if Tmatch:
                    return ['append',rule[index+step+1]]
                else:
                    try:
                        if rule[index+step+2] == '`':
                            return ['first',lhs,f'{rule[index+step+1]}`']
                        else:
                            return ['first',lhs,f'{rule[index+step+1]}']
                    except:
                        return ['first',lhs,f'{rule[index+step+1]}`']
                    
rules = readFile('LL(1) Parser/rules.txt')
printRules(rules)
rules = LeftRecursion(rules)
printRules(rules)
rules = LeftFactoring(rules)            
printRules(rules)
rules = maintainOrder(rules)
printRules(rules)
first = FindFirst(rules)
print('first:',first)
follow = FindFollow(rules)
printFF(first,follow,rules)
