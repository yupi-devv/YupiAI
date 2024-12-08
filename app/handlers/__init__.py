import os
from importlib import util



ii = os.getcwd()
a = ii.split('/')
dd = []
root = ''
if a[-1] == "handlers" and a[-3] == "YupiAI":
    path = os.getcwd() + '/'
    for i in os.walk(path):
        dd.append(i)
    dd = dd[0][-1]
elif a[-1] == "YupiAI":
    path = os.getcwd() + '/app/handlers/'
    for i in os.walk(path):
        dd.append(i)
    dd = dd[0][-1]
else:
    raise Exception("Вы не в той директории, запустите бота из его директории")


dd.remove('__init__.py')
routers = []
for i in dd:
    spec = util.spec_from_file_location(i, f"{path}{i}")
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    routers.append(module.rt)
tuple(routers)
#from app.handlers.start import rt as start
#from app.handlers.ss import rt as ss
#routers = (start, ss)