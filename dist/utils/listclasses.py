import ast
import os
 
def get_file_list(path):
    directories = os.listdir( path )
    return [file for file in directories if '__' not in file]

def show_info(functionNode):
    print("Function name:", functionNode.name)
    print("Args:")
    for arg in functionNode.args.args:
        #import pdb; pdb.set_trace()
        print("\tParameter name:", arg.arg)

def get_classes(path, l):
    c = []
    d = {}
    for i in l:
        with open(path+'/{}'.format(i)) as file:
            node = ast.parse(file.read())
        classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
        for class_ in classes:
            c.append(class_.name)
            d[class_.name] = i.strip('.py')+'.{}'.format(class_.name)
    return c, d
