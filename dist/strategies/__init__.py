import os

l = [i.name.split('.')[0] for i in os.scandir('dist/strategies') if '__' not in i.name]

for i in l:
    exec('from .{} import *'.format(i))
