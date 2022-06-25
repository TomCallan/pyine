import js2py
from series import Series

def functions(s):
    l = s.split('=>')
    name = s.split('=>')[0].split('(')[0]
    args = s.split('=>')[0].split('(')[-1].split(')')[0]
    f = l[-1]
    x = "{} = function $({})".format(name, args) + "{return" + f + "}"    
    return x

#for line in file:
#    # relace math with Math
#    if "?" and ":" in line:
#        js2py.eval_js(line)
#    if "=>":
#        functions(s)
        