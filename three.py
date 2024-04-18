def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    stack = []

    for char in expression:
        if char.isalnum():
            output.append(char)
        else:
            while stack and precedence.get(stack[-1], 0) >= precedence.get(char, 0):
                output.append(stack.pop())
            stack.append(char)

    while stack:
        output.append(stack.pop())

    return ''.join(output)


def generate_3ac(expression):
    postfix_expression = infix_to_postfix(expression)
    stack = []
    temp_count = 0
    three_address_code = []

    for token in postfix_expression:
        if token.isalnum():
            stack.append(token)
        elif token == '=':
            operand2 = stack.pop()
            operand1 = stack.pop()
            three_address_code.append((token, operand1, operand2, ''))
            print(f"{operand1} = {operand2}")
        else:
            operand2 = stack.pop()
            operand1 = stack.pop()
            temp_count += 1
            result = 't' + str(temp_count)
            three_address_code.append((token, operand1, operand2, result))
            stack.append(result)
            print(f"{result} = {operand1} {token} {operand2}")

    return three_address_code


def generate_triples(quadruples):
    triples = []
    index_map = {}  # Dictionary to store indexes associated with result
    for idx, (op, arg1, arg2, res) in enumerate(quadruples):
        if res not in index_map:
            index_map[res] = idx
        if arg1.startswith('t'):
            arg1 = f"[{index_map.get(arg1, arg1)}]"
        if arg2.startswith('t'):
            arg2 = f"[{index_map.get(arg2, arg2)}]"

        operand2 = arg2
        triples.append((op, arg1, operand2))
    return triples


if __name__== "__main__":
    expression = input("Enter a mathematical expression strictly without brackets: ")
    postfix_expression = infix_to_postfix(expression)
    print("Postfix expression:", postfix_expression)

    print("\n3AC Equations:")
    quadruples = generate_3ac(expression)

    print("\nQuadruples:")
    print("{:<10} {:<10} {:<10} {:<10} {:<10}".format("Index", "Operator", "Operand1", "Operand2", "Result"))
    for idx, equation in enumerate(quadruples):
        if equation[0] == '=':
            print("{:<10} {:<10} {:<10} {:<10} {:<10}".format(f"[{idx}]", *equation))
        else:
            print("{:<10} {:<10} {:<10} {:<10} {:<10}".format(f"[{idx}]", equation[0], equation[1], equation[2],
                                                              equation[3] if len(equation) == 4 else ''))

    print("\nTriples:")
    print("{:<10} {:<10} {:<10}".format("Operator", "Operand1", "Operand2"))
    triples = generate_triples(quadruples)
    for triple in triples:
        print("{:<10} {:<10} {:<10}".format(*triple))