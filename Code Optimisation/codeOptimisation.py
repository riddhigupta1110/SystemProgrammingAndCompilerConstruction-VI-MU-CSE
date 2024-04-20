import re

def constant_folding(expression):
    try:
        variable, expr = expression.split('=')
        result = eval(expr.strip())
        return f"{variable.strip()} = {result}"
    except:
        return expression

def separate_vars_operators(statement):
    pattern = r"([a-zA-Z0-9_]+|\W+)"  # Matches variables (letters, numbers, underscores) or operators
    return re.findall(pattern, statement)

def copy_propagation(input_lines):
    variables = {}
    output_lines = []
    replace = {}
    for line in input_lines:
        line = line.strip()
        if '=' not in line:
            continue
        assignment = line.split('=')
        variable = assignment[0].strip()
        expression = assignment[1].strip()
        modified_expression = ''
        # Check if the expression is already a variable
        if expression in variables.keys():
            replace[variable] = expression
        separated = separate_vars_operators(expression)
        for exp in separated:
            if (exp in replace.keys()):
                modified_separated = [element.replace(exp, replace[exp]) for element in separated]
                modified_expression = ''.join(modified_separated)
                output_lines.append(variable + ' = ' + modified_expression)
                continue
        if modified_expression == '':
            if variable in replace.keys():
                continue
            output_lines.append(variable + ' = ' + expression)
            variables[variable] = expression
    return output_lines

def common_subexpression_elimination(input_lines):
    expressions = {}
    output_lines = []
    for line in input_lines:
        assignment = line.split('=')
        variable = assignment[0].strip()
        expression = assignment[1].strip()
        for var, exp in expressions.items():
            expression = expression.replace(exp, var)
        output_lines.append(variable + ' = ' + expression)
        expressions[variable] = expression
    return output_lines

def optimize(input_file, output_file):
    with open(input_file, 'r') as f:
        input_lines = f.readlines()
    output_lines = [constant_folding(line) for line in input_lines]
    output_lines = copy_propagation(output_lines)
    output_lines = common_subexpression_elimination(output_lines)
    with open(output_file, 'w') as f:
        f.write('\n'.join(output_lines))
optimize('Code Optimisation/input.txt', 'Code Optimisation/output.txt')
