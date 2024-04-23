#code generation
# taking lines of code as input and processing them to generate
# assembly code which achieves the desired task
# output format --> statements, code, register, address desc

operators = ['+','-','*','/']
register = {}
temp_count = 0
rules = {}

operation = {
    '+':'ADD',
    '-':'SUB',
    '*':'MUL',
    '/':'DIV'
}
print('-'*103)
rowFormat = '{:<1} {:<10} {:<1} {:<30} {:<1} {:<30} {:<1} {:<20} {:<1}'
print(rowFormat.format('|','statement','|','code_gen','|','reg_desc','|','add_desc','|'))
    
def TablePrinter(lhs,rhs,op,code_gen,reg_desc,add_desc):
    statement = lhs+op+rhs
    print(rowFormat.format('|',statement,'|',code_gen,'|',reg_desc,'|',add_desc,'|'))

def generateTemp(temp_count):
    temp_count += 1
    return temp_count,f"t{temp_count}"

def readFile(fileName):
    with open(fileName,'r') as file:
        fileContent = file.read().split('\n')

    for line in fileContent:
        lhs,rhs = line.split('=')
        rules[lhs] = rhs

    return rules

def code_gen(lhs,rhs,op):
    code_gen = ""
    reg_desc = ""
    add_desc = ""
    variables = rhs.split(op)
    global temp_count
    #print(variables)
    if variables[0] not in rules.keys():
        temp_count,temp = generateTemp(temp_count)
        code_gen = f"MOV {variables[0]},R{temp_count},{operation[op]} {variables[1]},R{temp_count}"
        register[f"R{temp_count}"] = lhs
    else:
        if variables[1] in rules.keys():
            var1 = ''
            var2 = ''
            for reg,val in register.items():
                if val == variables[0]:
                    var1 = reg
                if val == variables[1]:
                    var2 = reg

            code_gen = f"{operation[op]} {var2},{var1}"
            register[var1] = lhs
        else:
            var1 = ''
            for reg,val in register.items():
                if val == variables[0]:
                    var1 = reg

            code_gen = f"{operation[op]} {variables[1]},{var1}"
            register[var1] = lhs

    for R,V in register.items():
        reg_desc = reg_desc + f"{R} contains {V},"
        add_desc = add_desc + f"{V} in {R},"

    print('-'*103)
    TablePrinter(lhs,rhs,'=',code_gen,reg_desc[:-1],add_desc[:-1])
    
def processing(rules):
    for lhs,rhs in rules.items():
        op = ""
        for i in operators:
            if i in rhs:
                op = i
                
        code_gen(lhs,rhs,op)
        lastVar = lhs
        
    lastReg = ""
    for reg,val in register.items():
        if val == lastVar:
            lastReg = reg

    code_gen1 = f"MOV {lastReg},{lastVar}"

    add_desc1 = f"{lastVar} in {lastReg} and memory"
    TablePrinter('','','',code_gen1,'',add_desc1)
    print('-'*103)

rules = readFile('TargetCode for 3AC/input.txt')
processing(rules)
    
