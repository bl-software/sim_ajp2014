# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
from Params.Param_Funcs import *
from Params.Param_Validators import *

class Param:
    def __init__(self, *args, **kwargs):
        #print('Param:',args[0])
        args=list(args)

        self.human_name = args.pop(0)
        self.mlvar_name = args.pop(0) # MATLAB Simulation Variable

        self.validator  = args.pop(0)
        self.formatter  = args.pop(0)

        self.disp_col   = args.pop(0)
        self.disp_grp   = args.pop(0)
        self.disp_type  = args.pop(0)

        valfromfile       = args.pop(0)
        #print('VFF=',valfromfile)
        if valfromfile == ['LUT']:
            self.allow_LUTs= True
        else:
            self.allow_LUTs= False
        #self.valstore          = valfromfile if not callable(valfromfile) else [] # all vals stored as list - even singles
        #self.callable_val      = valfromfile if callable(valfromfile) else self.default_callable_val
       
        ''' valfromfile is either:
            list with default vals
            tuple with func and its args '''
#        print('human_name:',self.human_name)
#        print('vff',valfromfile)
#        breakpoint()
        vff_v,*vff_args    = valfromfile
        self.valstore      = valfromfile if vff_v not in p_funcs else [] # all vals stored as list - even singles
        #print(self.human_name, 'valstore=',self.valstore, vff_v)
        self.callable_val  = vff_v       if vff_v     in p_funcs else self.default_callable_val # STRING for now - fix at post_init after params exists
        self.callable_args = vff_args

        self.onval      = args.pop(0)
        self.dependents = args.pop(0) # tuple of strings at this point - post_init changes to params after params exists

        self.is_in_dialog = True if self.disp_type in [ 'dtb', 'dcb', 'db' ] else False
        if self.is_in_dialog:
            self.disp_grp = 'd_' + self.disp_grp

        self.is_button = True if self.disp_type in ['b', 'db'] else False

        self.is_output = True if self.disp_type in ['otb', 'ocb'] else False

        self.is_textbox = True if self.disp_type in ['tb', 'dtb', 'otb'] else False

        self.is_checkbox = True if self.disp_type in ['cb', 'dcb', 'ocb'] else False
        
        self.is_string = True if self.validator is a_string else False

        self.is_choice = True if self.disp_type in ['ch'] else False

        self.is_hidden = True if self.disp_type in [''] else False

        if self.is_choice:
            self.choices = kwargs['choices']

    def post_init(self,params):
        self.params= params

#        print(self.callable_val)
#        print(self.default_callable_val)
#        print(p_funcs)
#        print(self.callable_val == self.default_callable_val)
#        print(self.callable_val is self.default_callable_val)
        if self.callable_val != self.default_callable_val:
            self.callable_val = p_funcs[self.callable_val]

        #print(self.mlvar_name, self.dependents )
        self.dependents = [ params[d] for d in self.dependents ]

    def set_valstore(self,l):
        try:
            #print('SVST:(',self.mlvar_name,'):',type(l),l)
            self.valstore = self.validator(l)
            #print('SVST:(',self.mlvar_name,'):VALID',self.valstore)
            return True
        except ValueError:
            #print('SVST:(',self.mlvar_name,') ValueError ---------------------------------------------------')
            return False

    def default_callable_val(self,*args):
        ''' returns list of vals '''
        return self.valstore

    def __call__(self):#,val_l=None):
        print('(##',self.mlvar_name,'##)')
        return self.callable_val(self.params,*self.callable_args) # either default_callable_val or user provided f_ function

def build_param_list(base_pl,new_pl):
    pl = {}
    for k,v in base_pl.items():
        if k not in new_pl:
            pl[k] = v
        else:   # this is to maintain order in original list
            pl[k] = new_pl.pop(k)
       
    # do remaining (extra) items
    for k,v in new_pl.items():
        pl[k] = v
    return pl

def create_params(pl):
    params= {}
    for k,(args,kwargs) in pl.items():
        params[k] = Param(*args,**kwargs)

    for p in params.values():
        p.post_init(params)

    return params

