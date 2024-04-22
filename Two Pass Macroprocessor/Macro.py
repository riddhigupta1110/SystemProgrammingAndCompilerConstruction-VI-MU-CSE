import re
import copy
from tabulate import tabulate

# Initialize variables
temp_input = []
mdt = []
ala = []
mnt = {}
mdt_copy = []

# Read the source.txt file and store it in temp_input list
with open('Two Pass Macroprocessor/source.txt', 'r') as input_file:
    temp_input = [line.strip() for line in input_file]

# PASS 1
# Store the lines from temp_input to mdt list
append = False
for line in temp_input:
    if line == 'MACRO':
        append = True
        continue
    if append:
        mdt.append(re.split(r'[, ]+', line))
        mdt_copy.append(re.split(r'[, ]+', line))
    if line == 'MEND':
        append = False

# Find macro start indices and names
mdt_index = {0}  # Stores the indices of macro start in mdt
macro_names = []  # Stores the macro names

for idx, item in enumerate(mdt):
    if 'MEND' in item and idx + 1 < len(mdt):
        mdt_index.add(idx + 1)

for index in mdt_index:
    macro_names.append(mdt[index][0])

# Stores the macro names and mdt indices in mnt dict
for macro_name, index in zip(macro_names, mdt_index):
    mnt[macro_name] = index

# Stores arguments in ala list
for index in mdt_index:
    for i in range(1, len(mdt[index])):
        arg = mdt[index][i]
        if arg.endswith('='):
            arg = arg[:-1]
        ala.append(arg)

pass1_ala = copy.copy(ala)

# Updates the mdt to replace the args with #indices from ala
for idx, line in enumerate(mdt):
    if idx not in mdt_index:
        for i, token in enumerate(line):
            if token in ala:
                line[i] = f',#{ala.index(token)+1}'

mdt_sentences = [' '.join(line) for line in mdt]

mnt_with_index = [(idx, k, v+1) for idx, (k, v) in enumerate(mnt.items(), start=1)]
print("\nPASS 1: \n")
print("MNT:")
print(tabulate(mnt_with_index, headers=['Index', 'Macro Name', 'MDT Index'], tablefmt="fancy_grid"))
print("\nALA:")
print(tabulate(enumerate(ala, start=1), headers=['Index', 'Arguments'], tablefmt="fancy_grid"))
print("\nMDT:")
print(tabulate(enumerate(mdt_sentences, start=1), headers=['Index', 'Macro definition'], tablefmt="fancy_grid"))

# PASS 2
temp_input = [re.split(r'[, ]+', line) for line in temp_input]
mend_loc = None

# Store the last occurrence of 'MEND'
for line_num, line in enumerate(temp_input):
    if 'MEND' in line:
        mend_loc = line_num

# Empty the ala list and add arguments (data) in ala list
ala.clear()
print(temp_input)
for line in temp_input[mend_loc+1:]:
    for idx, item in enumerate(line):
        if item in macro_names:
            next_items = line[idx+1:]
            for next_item in next_items:
                if '=' in next_item:
                    next_item = next_item.split('=')[-1]
                ala.append(next_item)

# Only store unique arguments
temp_ala = []
for item in ala:
    if '=' in item:
        item = item.split('=')[-1]
    if item not in temp_ala:
        temp_ala.append(item)

# Maps the args in macro def to args passed when macro is called
arg_data_map = {}
for pass1_ala, pass2_ala in zip(pass1_ala, ala):
    arg_data_map[pass1_ala] = pass2_ala

# Modify macro definitions in mdt_copy
for index in mdt_index:
    for idx, item in enumerate(mdt_copy[index]):
        if '=' in item:
            mdt_copy[index][idx] = item.split('=')[0]

# Change the occurrences of args to data using dictionary
for sublist in mdt_copy:
    for idx, value in enumerate(sublist):
        if value in arg_data_map:
            sublist[idx] = arg_data_map[value]

mdt_sentences_copy = [' '.join(line) for line in mdt_copy]

print("\nPASS 2:")
print("\nALA:")
print(tabulate(enumerate(temp_ala, start=1), headers=['Index', 'Arguments'], tablefmt="fancy_grid"))
print("\nMDT:")
print(tabulate(enumerate(mdt_sentences_copy, start=1), headers=['Index', 'Macro definition'], tablefmt="fancy_grid"))
