from pymake.filepatterns import filepattern, nameiterator, FP_MODE_WC, FP_MODE_PAT

fp1=filepattern("pat*lol*.ch%.txt")
fp2=filepattern("pat%1lol%2.ch%%.txt",FP_MODE_PAT)
print("Native WC:"),
print(fp1.wc)
print("Contructed Pat:"),
print(fp1.pat)
print("RE:"),
print(fp1.re)
print("")
print("Native Pat:"),
print(fp2.pat)
print("Constructed WC:"),
print(fp2.wc)
print("RE:"),
print(fp2.re)


print("Equallity:")
print(fp1==fp2)
