from pymake import *

@requires("test.py")
@withrequires("run-%1.txt")
@pmk.makemany("run-*.%.txt")
def createlines(main,other):
    with open(other) as f:
        for l in f:
            fn=main.next()
            with open(fn,'w') as fs:
                fs.write(l)

pmk.trigger("run-bad.0.txt")
