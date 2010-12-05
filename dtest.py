import sys, pdb
class TestPdb(pdb.Pdb):
    def __init__(self, *args, **kwargs):
        self.__stdout_old = sys.stdout
        sys.stdout = sys.__stdout__
        pdb.Pdb.__init__(self, *args, **kwargs)

    def cmdloop(self, *args, **kwargs):
        sys.stdout = sys.__stdout__
        retval = pdb.Pdb.cmdloop(self, *args, **kwargs)
        sys.stdout = self.__stdout_old

def set_trace():
    debugger = TestPdb()
    debugger.set_trace(sys._getframe().f_back)

