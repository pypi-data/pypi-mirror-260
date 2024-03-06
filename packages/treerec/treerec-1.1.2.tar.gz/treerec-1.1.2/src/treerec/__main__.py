from treerec.trcursor import TreeObj_Cursor

import os
if os.name=='nt':
    try:
        import win32security
    except:
        print('   ***')
        print('WARNING: on Windows systems, `pywin32` package must be installed for treerec to record files'' owners.')
        print('   ***')

C = TreeObj_Cursor()
print_welcome = True
while not C.time_to_leave:
    try:
        C.mainloop(print_welcome)
    except Exception as error:
        print('-----------///-----------')
        print(error)
        print('-----------///-----------')
        print_welcome = False