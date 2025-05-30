#############
DBG_PF  =0x01 # Papers Figs
DBG_DIRS=0x02 # Papers Figs
DDEPS   =0x04
#############
DBG     =0x07
#############
def dprint(d,*what):
    if d & DBG:
        try:
            for item in what:
                print(item, end=' ')
            print()
        except SyntaxError as se:
            print('PY3',)
            print(what)

hands='👉'*5
def hprint(*what):
    print(hands,*what)


