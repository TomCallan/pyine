import js2py

def functions(s):
    l = s.split('=>')
    name = s.split('=>')[0].split('(')[0]
    args = s.split('=>')[0].split('(')[-1].split(')')[0]
    f = l[-1]
    x = "{} = function $({})".format(name, args) + "{return" + f + "}"    
    return x