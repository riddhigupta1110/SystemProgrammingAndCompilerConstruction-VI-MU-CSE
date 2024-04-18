def precedence(c):
   if c == '/' or c == '*':
       return 2
   elif c == '+' or c == '-':
       return 1
   else:
       return -1

def infix_to_postfix(s):
   result = []
   stack = []
   assignment_operator = False
   assignment = ""
   for i in range(len(s)):
       c = s[i]
       if ('a' <= c <= 'z') or ('A' <= c <= 'Z') or ('0' <= c <= '9'):
           result.append(c)
       elif c == '(':
           stack.append(c)
       elif c == ')':
           while stack and stack[-1] != '(':
               result.append(stack.pop())
           stack.pop()
       elif c == '=':
           assignment_operator = True
           assignment = result.pop()
       else:
           while stack and (precedence(s[i]) <= precedence(stack[-1])):
               result.append(stack.pop())
           stack.append(c)
   while stack:
       result.append(stack.pop())
   if assignment_operator:
       result.extend([assignment, '='])
   return result

def check_3ac(operation, dict_3ac):
   for key, value in dict_3ac.items():
       if value == operation:
           return key
   return False

def convert_to_3ac(expression):
   count = 0
   three_ac_dict = dict()
   operand = list()
   for i, item in enumerate(expression):
       if item == '+' or item == '-' or item == '/' or item == '*':
           op2 = operand.pop()
           op1 = operand.pop()
           in_3ac = check_3ac(f'{op1}{item}{op2}', three_ac_dict)
           if not in_3ac:
               count += 1
               three_ac_dict[f't{count}'] = f'{op1}{item}{op2}'
               operand.append(f't{count}')
           else:
               operand.append(in_3ac)
       elif item == '=':
           three_ac_dict[operand.pop()] = f't{count}'
       else:
           operand.append(item)
   return three_ac_dict

def convert_to_quadruples(address_code_dict):
   quadruple_list = dict()
   list_no = 0
   for key, value in address_code_dict.items():
       if len(value) <= 2:
           i = value.find('=')
           quadruple_list[list_no] = {
            "op": "=", 
            "arg1": value, 
            "arg2": "   ", 
            "result": key
            }
           list_no += 1
       else:
           for item in ['-', '+', '*', '/']:
               if item in value:
                   i = value.find(item)
                   quadruple_list[list_no] = {
                    "op": value[i],
                    "arg1": value[:i], 
                    "arg2": value[i + 1:],
                    "result": key 
                    }
               else:
                   continue
           list_no += 1
   return quadruple_list

def convert_to_triples(quadruples_dict):
   triples_dict = dict()
   dict_no = 0
   for key1, value1 in quadruples_dict.items():
       if value1['op'] == "=":
           triples_dict[dict_no] = { 'op': value1['op'], 'arg1': value1['result'],
               'arg2': f"({int(value1['arg1'][-1]) - 1})" if "t" in value1['arg1'] else value1['arg1']
           }
       else:
           triples_dict[dict_no] = { 'op': value1['op'], 'arg1': f"({int(value1['arg1'][-1]) - 1})" if "t" in    value1['arg1'] else value1['arg1'],
               'arg2': f"({int(value1['arg2'][-1]) - 1})" if "t" in value1['arg2'] else value1['arg2']
           }
       dict_no += 1
   return triples_dict

statement = input("Statement: ")  # x=a+a*(b-c)+(b-c)/d
postfix = infix_to_postfix(statement)
address_codes = convert_to_3ac(postfix)

print("\nTHREE ADDRESS CODE")
for key, value in address_codes.items():
   print(f'{key} = {value}')
quadruples = convert_to_quadruples(address_codes)

print("\nQUADRUPLES")
print("\top  arg1  arg2  result")
for key, value in quadruples.items():
   print(f"{key}\t{value['op']}\t {value['arg1']}\t\t{value['arg2']}\t {value['result']}")
triples = convert_to_triples(quadruples)

print("\nTRIPLES")
print("\top  arg1  arg2")
for key, value in triples.items():
   print(f"{key}\t{value['op']}\t {value['arg1']}\t{value['arg2']}")
