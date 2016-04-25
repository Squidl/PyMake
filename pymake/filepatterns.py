import re

FP_MODE_WC=1002
FP_MODE_PAT=1003

class filepattern(object):
    def __init__(self,string,mode=None):
        self.orig=string
        if mode==None or mode==FP_MODE_WC:
            self.init_as_wildcard(string)
        elif mode==FP_MODE_PAT:
            self.init_as_pat(string)
        self.compilepat()
    def compilepat(self,):
        try:
            self.matcher=re.compile(self.re)
        except:
            print("Error compiling:"),
            print(self.re)
            #exit(1)
    def __eq__(self,other):
        return self.pat==other.pat
    def init_as_wildcard(self,string):
        self.wc=string
        pat=re.escape(string)
        pat=pat.replace("\*","(.*)")
        pat=pat.replace("\%","(.*)")
        if pat[0]!='^':
            pat='^'+pat
        if pat[-1]!='$':
            pat=pat+'$'
        self.re=pat
        pat=str(string)
        wilds=[]
        for i in range(len(pat)):
            if pat[i]=='*':
                wilds.append(("*",i))
            elif pat[i]=='%':
                wilds.append(("%",i))
        offset=0
        c=1
        for i in range(len(wilds)):
            wild=wilds[i]
            ind=wild[1]+offset
            if wild[0]=="*":
                pat=pat[:ind]+"%"+str(c)+pat[ind+1:]
                offset=offset+1
                c=c+1
            else:
                pat=pat[:ind]+"%%"+pat[ind+1:]
                offset=offset+1
        self.pat=pat
    def init_as_pat(self,string):
        self.pat=string
        pat=re.escape(string)
        ind=pat.find("\%")
        wc=""
        pats=[]
        varl=[]
        while ind!=-1:
            var=pat[ind+2]
            pats.append(pat[:ind])
            if var=="\\" and pat[ind+3]=="%":
                var=pat[ind+3]
                pat=pat[ind+4:]
            else:
                pat=pat[ind+3:]
            varl.append(var)
            ind=pat.find("\%")
        pats.append(pat)
        pat="(.*)".join(pats)
        wc=""
        for i in range(len(varl)):
            wc=wc+pats[i]+("%" if varl[i]=="%" else "*")
        wc=wc+pats[len(varl)]
        if pat[0]!='^':
            pat='^'+pat
        if pat[-1]!='$':
            pat=pat+'$'
        self.re=pat
        self.wc=wc
    def match(self,string):
        return self.matcher.match(string)

    def format(self,m):
        groups=m.groups()
        pat=str(self.pat)
        for j in range(len(groups)):
            pat=pat.replace("%"+str(j+1)[0],groups[j])
        return pat.replace("\\","")
    def formatmany(self,m,i):
        s=self.format(m)
        s.replace("%%",i)
        return s

class nameiterator(object):
    def __init__(self,pat):
        self.pat=pat
        self.count=0
    def next(self):
        self.count=self.count+1
        returner=str(self.pat)
        return returner.replace("%",str(self.count))
    
