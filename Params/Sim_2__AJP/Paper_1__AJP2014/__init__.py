import os
from ... import importer, showimp
indent=__name__.count('.')*'  '

showimp(indent, __name__, __path__, __file__)

Params= Storage_d= {}
_glb={'prefix':'Params_',
      'testf' :os.path.isfile}
importer(indent,_glb,Params,__name__)

