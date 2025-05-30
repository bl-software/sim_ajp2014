import glob ,os, re
import math
import importlib
import pprint
indent=__name__.count('.')*'  '

def dprint(*margs):
    pass
    #breakpoint()
    #print(*margs)

def showimp(indent,name,path,file):
    dprint('\n')
    if path:
        dprint(f'{indent}{name}:__path__=',path)
    if name:
        dprint(f'{indent}{name}:__name__=',name) # "Params"
    if file:
        dprint(f'{indent}{name}:__file__=',file) # "Params"

fpattern= re.compile(r'.*_(\d+)__.*')
def forder(fn):
    #dprint(f'Figures/__init__:fn={fn}')
    match=fpattern.match(fn)
    if not match:
        return math.inf
    return int(match.groups()[0])


def importer(indent,glb,storagedict,name):
    #indent=f'imp{indent}'
    glbpre=glb['prefix']
    glbtst=glb['testf']
    #dprint('glbpre=',glbpre)
    _namepath= name.replace('.','/')
    dprint(f'{indent}{_namepath}: glb=',glb)
    tstsp= ' ' * (len(glbpre) + 4 -len('tested'))
    _globmatches=glob.glob(f'{_namepath}/{glbpre}*')
    dprint(f'{indent}{_namepath}: _globmatches=(glob{tstsp}    :: {_globmatches}')
    _globmatches= sorted(_globmatches, key=forder)
    dprint(f'{indent}{_namepath}: _globmatches=(pre={glbpre}) :: {_globmatches}')
    _globmatches= [ g for g in _globmatches if glbtst(g) ]
    dprint(f'{indent}{_namepath}: _globmatches=(tested){tstsp} :: {_globmatches}')

    _modnames=[ os.path.basename(os.path.normpath(f)).removesuffix('.py') for f in _globmatches ]
    dprint(f'{indent}{_namepath}: _modnames=',_modnames)

    shortpattern=f'{glbpre}\d+__'
    for modname in _modnames:
        dprint(f'\n{indent}{_namepath}: doing modname:',modname)
        #shortmodname= modname.replace(glbpre,'')
        shortmodname= re.sub(shortpattern, '', modname)
        dprint(f'{indent}{_namepath}: shortmodname=',shortmodname)
        #dprint(f'{_namepath}: mn:{modname} pn:{name}')
        module = importlib.import_module('.'+modname, package=name)
        try:
            if glbpre == 'Figure_':
                dprint(f'{indent}{_namepath}: Storing Figure')
                storagedict[shortmodname]=module.Fig
            else:
                dprint(f'{indent}{_namepath}: Storing Storage_d Module')
                storagedict[shortmodname]=module.Storage_d
        except AttributeError:
            dprint(f'{indent}Need to Define "Storage_d or Fig" in  {module}')

    #dprint(f'{indent}{_namepath}:Storage_d=',pprint.pformat(storagedict))
    #pprint.pp(storagedict)

showimp(indent, __name__, __path__, __file__)

Figs= Sims= Storage_d= {}
_glb={'prefix':'Sim_',
      'testf' :os.path.isdir}
importer(indent,_glb,Storage_d,__name__)

#pprint.pp(Figs)
#breakpoint()


