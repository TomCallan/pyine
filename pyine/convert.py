import re

# misc
def comment(line):
    _ = False
    if re.findall("strategy|study|plot|//", line):
        line = line.split(' ')
        line.insert(0, '#')
        line = ' '.join(line)
        _ = True
    return line, _

# logic >>>> add more logic support
def logic(line):
    if re.findall("if ", line):
        line = line.split(' ')
        line[-1] = line[-1].strip('\n')
        line.append(':\n')
        line = ' '.join(line)
    return line

# booleans
def boolean(line):
    boolx = re.findall("true|false", line)
    for booly in boolx:
        string = line.split(booly)
        booly = booly.replace(" ", "").capitalize()
        string.insert(-1, booly)
        line = ''.join(string)
    return line

# operators
def operator(line):
    op = re.findall("\?|:=", line)
    op.append(' ')
    if op[0] == ':=':
        string = line.split(op[0])
        op[0] = '='
        string.insert(-1, op[0])
        line = ''.join(string)

    if op[0] == '?':
        try:
            s1 = line.split("=")
            string = s1[-1].replace(" ", "")
            string = string.split(op[0])
            condition = string[0].replace(" ", "")
            sub = string[1].replace(" ", "")
            sub = sub.split(":")
            val1 = str(sub[0])
            val2 = str(sub[1])
            var = s1[0].replace(" ", "")
            if var and condition and val1 and val2:
                string = '{0} = lambda {1}, {2}, {3}: {2} if {1} else {3}'.format(var, condition, val1, val2)
            else:
                string = 'failed to interpret line, make sure it is formatted as:\na = b ? c : d'
            line = string
        except Exception as e:
            line = 'failed to interpret line, make sure it is formatted as:  na = b ? c : d'
    return line

# builtins >>>>> add more builtin function support 
def builtins(line):
    funcx = re.findall("input\(|alert\(", line)
    funcx.append(' ')
    if funcx != [' ']:
        funcy = funcx[0]
        if funcy == 'alert(':
            string = line.split(funcy)
            funcy = funcy.replace("alert(", "print(")
            string.insert(-1, funcy)
            line = ''.join(string)
        if funcy == 'input(':
            line = '# pyine does not currently support inputs [{0}]\n'.format(line.strip('\n'))
    return line

# functions
def functions(line):
    funcx = re.findall("=>", line)
    if funcx:
        line = line.split(funcx[0])
        n1 = line[0].replace(" ", "")
        n2 = line[1].replace(" ", "")
        if '\t' not in n2:
            string = 'def {0}:\n\t{1}'.format(n1, n2)
        else:
            string = 'def {0}:\n{1}'.format(n1, n2)
        line = string
    return line





## MAIN
def convert(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        filename = file.split(".")[0]
    
    with open('{0}.py'.format(filename), 'w') as f:  
        f.write('from pyine.indicators import *\n\n')
        for line in lines:
            line, c = comment(line)
            if not c:
                line = functions(logic(boolean(operator(functions(line)))))
            #print(line)
            f.write(line)
