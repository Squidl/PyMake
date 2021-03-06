from pymake import *

@requires("test.py")
@withrequires("third%1.py")
@pmk.make("fourth*.py")
def createnoo(main,other):
    print(main)
    print(other)

@requires("test.py")
@withrequires("sec%1.txt")
@pmk.make("third*.py")
def rump(out,inp):
    with open(inp) as finp:
        with open(out,'w') as fout:
            fout.write(finp.read())

@requires("test.py")
@withrequires("first.txt")
@pmk.makestreams("sec*.txt")
def rumpt(out,inp):
    out.write(inp.read())

pmk.trigger("fourth01.py")
