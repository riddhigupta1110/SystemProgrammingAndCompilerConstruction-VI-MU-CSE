import re,os

# global variables
leftRecursion = []
leftFactoring = {}
first = {}
follow = {}

terminals = []
variables = []

epsilon = '\u03B5'

ruleFormat = '{:<2} {:<2} {:<50}'

def printRules(rules):
    for lhs,rhs in rules.items():
        rhsString = ""
        for i in rhs:
            rhsString = rhsString + i + " | "
        print(ruleFormat.format(lhs,'-->',rhsString[:-2]))
    # print("\n")

def printFF(rules):
    for lhs,rhs in rules.items():
        rhsString = "{"
        for i in rhs:
            rhsString = rhsString + i + " , "
        rhsString = rhsString[:-2]+"}"
        print(ruleFormat.format(lhs,'-->',rhsString))
    # print("\n")

def readFile(fileName):
    rules = {}
    try:
        with open(fileName,'r') as file:
            # read each line
            fileContent = file.read().split('\n')
        for rule in fileContent:
            # for each line, split into left and right
            lhs,rhs = rule.split("->")
            # replace epsilon wwith unicode character
            if '\\u03B5' in rhs:
                rhs.replace('\\u03B5',epsilon)
            rules[lhs] = rhs.split("|")
        return rules
    except FileNotFoundError:
        print('File not found error')

def LR_removal(rules):
    # print('CHECKING FOR LEFT RECURSION')
    for lhs,rhs in rules.items():
        # print(lhs,rhs)
        if lhs == rhs[0][0]:
            leftRecursion.append(lhs)
    
    if not len(leftRecursion):
        print('\nThere is no left recursion')
        return rules
    
    # left recursion removal
    for lhs in leftRecursion:
        alpha = []
        beta = []
        # if the first rhs of the rule is single letter 
        #? eg L -> L
        if len(rules[lhs][0]) == 1:
            pass
        else:
            # append all the remaining letters of the rhs to the alpha
            alpha.append(rules[lhs][0][1:])
        # all the rhs except the one with recursion are added as the beta for new rule
        beta = rules[lhs][1:]

        # print(alpha,beta)

        #? change the existing rule
        # new rule is beta followed by the actuall rule NT
        rules[lhs] = [f'{i}{lhs}`' for i in beta]
        # new rule is alpha followed by new NT, epsilon
        rules[f'{lhs}`'] = [f'{alpha[0]}{lhs}`',epsilon]
    return rules        

def lfremoval(rules):
    alpha = []
    for lhs,rhs in rules.items():
        alpha = []
        if len(rhs) == 1:
            continue
        for index,right in enumerate(rhs):
            if index == 0:
                continue
            # print(os.path.commonprefix([rhs[0],right]))
            temp =  os.path.commonprefix([rhs[0],right])
            alpha = temp if len(temp) > len(alpha) else alpha
        if len(alpha):
            leftFactoring[lhs] = alpha
    
    if not len(leftFactoring):
        print('There is no left factoring in the rules')
        return rules
    
    # left factoring removal
    for lhs,a in leftFactoring.items():
        alpha = []
        beta = []
        gamma = []

        alpha.append(a)
        # beta pattern : the part along the alpha in the rules
        beta_pattern = re.compile(f'{re.escape(alpha[0])}(.*)')

        # iterate through the rules to find beta and gamma
        for rhs in rules[lhs]:
            match = re.match(beta_pattern,rhs)
            if match:
                beta.append(match.group(1))
            else:
                gamma.append(rhs)

        # creation of new rules
        rules[lhs] = [f"{alpha[0]}{lhs}`"]
        for i in gamma:
            rules[lhs].append(i)

        # dash rule
        rules[f"{lhs}`"] = []
        for i in beta:
            rules[f"{lhs}`"].append(i)

    return rules

def maintainOrder(rules):
    newRules = {}
    for lhs,rhs in rules.items():
        if not lhs in newRules:
            newRules[lhs] = rules[lhs]
            if f"{lhs}`" in rules:
                newRules[f"{lhs}`"] = rules[f"{lhs}`"]
    return newRules

def findFirst(rules):
    # match the terminals which are between a-z,+, -, *, /, \, (, ),{, }, [, ] or $
    Tpattern = re.compile("[a-z]+|\+|\-|\*|\/|\(|\)|\{|\}|\$|\[|\]")
    # match the non terminals with A-Z or A`-Z`` etc, with ` optional
    NTpattern = re.compile("[A-Z]`?")
    for lhs,rhs in reversed(rules.items()):
        for i in rhs:   
            # check if the first character of the rule 
            # is terminal or not
            NTmatch = NTpattern.match(i[0])
            #? first character not a Variable (match failure)
            if NTmatch == None:
                # check for match with terminals, obtain the terminal
                Tmatch = Tpattern.match(i)
                if not lhs in first:
                    first[lhs] = []
                first[lhs].append(Tmatch[0] if Tmatch != None else epsilon)
            else: #? variable match found
                if not lhs in first:
                    first[lhs] = []
                # append the first of the encountered variable to the
                # existing lhs being traversed atm
                for f in first[NTmatch[0]]:
                    first[lhs].append(f)
    printFF(first)

def findFollow(LHS,rules):
    Tpattern = re.compile("[a-z]+|\+|\-|\*|\/|\(|\)|\{|\}|\$|\[|\]")
    step = 0 if len(LHS) == 1 else 1
    for lhs,rhs in rules.items():
        index = -1
        if lhs == LHS:
            continue
        for rule in rules[lhs]:
            # find index of the LHS in the rule
            try:
                index = rule.find(LHS)
                # print("->",index,rule,LHS)
                if index == -1:
                    continue
            except:
                print("Error")
            # check if the var is normal or followed by a `
            try:
                # if LHS does not contain ` originally skip
                if len(LHS) == 1 and rule[index+1] == '`':
                    continue
            except:
                print("")
            
            # print(index)
            if index+step == len(rule)-1:    #? the encountered variable is at the last
                #todo therefore use the follow of the original lhs
                return ['follow',lhs]
            #? check if var is followed by var or terminal and return
            elif index+step < len(rule)-1:
                #? followed by var
                if Tpattern.match(rule[index+step+1]):
                    return ['append',rule[index+step+1]]
                else:
                    try:
                        if rule[index+step+2] == '`':
                            return ['first',lhs,f"{rule[index+step+1]}`"]
                        else:
                            return ['first',lhs,rule[index+step+1]]
                    except:
                        return ['first',lhs,rule[index+step+1]]

def Follow(rules):
    Tpattern = re.compile("[a-z]+|\+|\-|\*|\/|\(|\)|\{|\}|\$|\[|\]")
    NTpattern = re.compile("[A-Z]`?")
    # initialising the follow with $ symbol
    # follow[rules[0]] = ['$']
    for lhs,rhs in rules.items():
        if not follow:
            follow[lhs] = ['$']
        step = 0 if len(lhs) == 1 else 1
        valueRet = findFollow(lhs,rules)
        # print(valueRet,lhs,follow)
        if valueRet[0] == "append":
            if not lhs in follow:
                follow[lhs] = []
            follow[lhs].append(valueRet[1])
        elif valueRet[0] == "follow":
            if lhs not in follow:
                follow[lhs] = []
            for i in follow[valueRet[1]]:
                follow[lhs].append(i)
        else:   #? first to be appended
            if lhs not in follow:
                follow[lhs] = []
            for i in first[valueRet[2]]:
                if i != epsilon:
                    follow[lhs].append(i)
                else:
                    ruleCopy = rules[valueRet[1]]
                    ruleCopy[0].replace(valueRet[2],"")
                    index = ruleCopy[0].find(lhs)
                    print(index)
                    try:
                        if index + step + 1 <= len(ruleCopy)-1:
                            if Tpattern.match(ruleCopy[0][index+step+1]):
                                follow[lhs].append(ruleCopy[0][index+step+1])
                            else:
                                var = ruleCopy[0][index+step+1]
                                for j in first[var]:
                                    follow[lhs].append(j)
                        else:
                            for j in follow[valueRet[1]]:
                                follow[lhs].append(j)
                    except:
                            print("")
    printFF(follow)


rules = readFile('LL(1) Parser/rules.txt')
print('\nGRAMMAR RULES')
printRules(rules)

#? left recursion removal
rules = LR_removal(rules)
print('\nThe rules after recursion Removal are :')
printRules(rules)

#? left factor removal
rules = lfremoval(rules)
print('\nThe rules after Left Factoring removal are :')
printRules(rules)

rules = maintainOrder(rules)
print("\n")
printRules(rules)

#? finding first
print("Finding Firsts:")
findFirst(rules)

#? find Follow
print("Finding follows: ")
Follow(rules)