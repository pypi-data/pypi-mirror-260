import treerec as tr
import os

os.chdir('../../treerec/test')
C = tr.TreeObj_Cursor()
C.execute('session Test')
C.execute('create new NewDev new.tree')
C.execute('recroot -n One -p O:/Test/ test1')
C.execute('recroot -n Four -p F:/Trial/ test4')
C.execute('recroot -n Bug -p B:/Linux buggy')
welcome = True
C.mainloop()
while not C.time_to_leave:
    try:
        C.mainloop(welcome)
    except Exception as error:
        print('--///--')
        print(error)
        print('--///--')
        welcome = False