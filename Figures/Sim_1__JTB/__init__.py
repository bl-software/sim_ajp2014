import os
from .. import importer, showimp
indent=__name__.count('.')*'  '
showimp(indent, __name__, __path__, __file__)

Papers= Storage_d= {}
_glb={'prefix':'Paper_',
      'testf' :os.path.isdir}
importer(indent,_glb,Papers,__name__)

