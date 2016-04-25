import traceback
import re
import os.path

from filepatterns import filepattern, nameiterator, FP_MODE_WC, FP_MODE_PAT

MAKE_MODE_NORMAL=1022
MAKE_MODE_STREAMS=1023
MAKE_MODE_MANY=1024

class makeitem(object):
    def __init__(self,makefile,pat,func,mode=MAKE_MODE_NORMAL):
        self.makefile=makefile
        self.pat=filepattern(pat)
        self.matcher=self.pat
        self.func=func
        self.reqs=[]
        self.args=[]
        self.mode=mode
    def match(self,f):
        return self.matcher.match(f)
    def __call__(self,m):
        if isinstance(m,str):
            tmpm=self.match(m)
            if tmpm is None:
                print("Cannot match: "),
                print(m),
                print("to :"),
                print(self.pat)
                exit(1)
            m=tmpm
        filename=m.group(0).replace("\\","")
        fmtime=None
        dochain=False
        if os.path.isfile(filename):
            fmtime=os.path.getmtime(filename)
        for i in self.reqs:
            formatpat=i.format(m)
            pmtime=None
            self.makefile.trigger(formatpat)
            if os.path.isfile(formatpat):
                pmtime=os.path.getmtime(formatpat)
            doreload=(fmtime < pmtime)
            if fmtime is None or pmtime is None or doreload:
                dochain=True
        if dochain:
            print("Triggered: "+filename)
            args=[filename]
            for i in self.args:
                args.append(i.format(m))
            try:
                if self.mode==MAKE_MODE_STREAMS:
                    nargs=[open(args[0],'w')]
                    for n in args[1:]:
                        nargs.append(open(args[1],'w+'))
                    r=self.func(*nargs)
                    for n in nargs:
                        n.close()
                    return r
                elif self.mode==MAKE_MODE_MANY:
                    nargs=args[1:]
                    return self.func(nameiterator(args[0]),*nargs)
                else:
                    return self.func(*args)
            except Exception as e:
                print("Error for trigger:"),
                print(filename)
                traceback.print_exc()
                exit(1)
        else:
            return True
        
class pymakefile(object):
    def __init__(self):
        self.items=[]
    def make(self,pat):
        def makedeff(func):
            item=makeitem(self,pat,func)
            self.items.append(item)
            return item
        return makedeff
    def makestreams(self,pat):
        def makestreamsdef(func):
            item=makeitem(self,pat,func,MAKE_MODE_STREAMS)
            self.items.append(item)
            return item
        return makestreamsdef
    def makemany(self,pat):
        def makemanydef(func):
            item=makeitem(self,pat,func,MAKE_MODE_MANY)
            self.items.append(item)
            return item
        return makemanydef
    def trigger(self,filename=None):
        if filename is None:
            return self.trigger(self.items.keys()[0])
        done=False
        trigs=self.items
        for trig in trigs:
            m=trig.match(filename)
            if m:
                trig(m)
                done=True
        if not done:
            if not os.path.isfile(filename):
                print("Error: could not find required: %s"%filename)
                exit() 
        

class requires(object):
    def __init__(self,pat):
        self.pat=pat
    def __call__(self,item):
        item.reqs=[filepattern(self.pat,FP_MODE_PAT)]+item.reqs
        return item

class withrequires(object):
    def __init__(self,pat):
        self.pat=pat
    def __call__(self,item):
        fp=filepattern(self.pat,FP_MODE_PAT)
        item.reqs=[fp]+item.reqs
        item.args=[fp]+item.args
        return item

pmk=pymakefile()
