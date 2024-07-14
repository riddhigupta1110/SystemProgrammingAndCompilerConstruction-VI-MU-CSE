# SystemProgrammingAndCompilerConstruction-VI-MU-CSE
Codes for Practical experiments of System Programming And Compiler Construction (Semester VI - Computer Engineering - Mumbai University)

Experiment List:
1. To create your own library using macros
2. To design lexical analyzer for a language whose grammar is known
3. To study and the implementation of lex and yacc tool
(A)To implement LEX PROGRAMS using Dev-Cpp
4. To design and implement a program for LL(1) parser
5. To generate 3-address code as an intermediate code representation
6.(A)Implementation of Code Optimization Techniques
(B)Implementation of Target code generation phase of the compiler
7. Implementations of two pass Macro Processor

## Prerequisites

1. Ensure you have Python 3.x installed on your machine. You can download it from [Python's official website](https://www.python.org/downloads/).
2. Ensure you have Flex(fast lexical analyzer generator) installed on your machine at "C:\GnuWin32". You can download it from [Flex download link](https://sourceforge.net/projects/gnuwin32/files/flex/2.5.4a-1/flex-2.5.4a-1.exe/download).
3. Ensure you have Bison(Yacc-compatible parser generator) installed on your machine at "C:\GnuWin32. You can download it from [Bison download link](https://sourceforge.net/projects/gnuwin32/files/bison/2.4.1/bison-2.4.1-setup.exe/download).
4. Ensure you have Dev C++ installed on your machine at "C:\Dev-Cpp". You can download it from [DEV C++ Download link](https://sourceforge.net/projects/orwelldevcpp/).
5. Open Environment Variables and add "C:\GnuWin32\bin" and "C:\Dev-Cpp\MinGW64\bin" to path. (If the path is different, ensure you add the correct bin path)

## Installation
1. Clone the repository
```bash
git clone https://github.com/riddhigupta1110/SystemProgrammingAndCompilerConstruction-VI-MU-CSE.git
```
2. Navigate to the project directory:
```shell
cd SystemProgrammingAndCompilerConstruction-VI-MU-CSE
```

## Usage
### **I) Python Programs:**
You can run each Python program using any code editor or the command line:

Using Visual Studio Code:
1. Open Visual Studio Code.
2. Open the project folder (SystemProgrammingAndCompilerConstruction-VI-MU-CSE) in VS Code.
3. Open the desired .py file.\n
4. Run the program by pressing F5 or by clicking the "Run" button in the top-right corner of the editor.

### **II) Lex Programs:**
### Study material:
- [Lex Programming Basics](https://www.ibm.com/docs/zh/aix/7.1?topic=l-lex-command)
- [Reference Video for downloading](https://youtu.be/7Xs21JKSHMc?si=ls9N7TofMmG3o9UB)

### To save Lex files: 
1. Save your Lex files with “.l” extensions in any specific directory
2. Open Command prompt and switch to your working directory where you have stored your lex file (“.l“)

### For Compiling and Executing Lex file:
Use the following commands in the same order as mentioned:

1.
```bash
flex file_name
```
2.
```bash
gcc lex.yy.c
```
3.
```bash
a.exe
```
### **III) Macros:**
You can run on Dev C++ by:
1. Save the .c and .h file
2. Compile the .c file
3. Run the .c file
4. Incase of issues in compiling and/or running, use the following command:
```bash
gcc filename.c -o filename
```
