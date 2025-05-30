import os
from ... import importer, showimp
indent=__name__.count('.')*'  '
showimp(indent, __name__, __path__, __file__)

Figs= Storage_d= {}
_glb={'prefix':'Figure_',
      'testf' :os.path.isfile}
importer(indent,_glb,Figs,__name__)

