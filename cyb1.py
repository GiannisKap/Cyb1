import random
from fractions import gcd
from sympy import mod_inverse

def bitSeq(mes):
    a=[]
    d2=[]
    for i in mes:
        x=format(ord(i), 'b')
        if len(x)==6:
            x='0'+x
        for j in range(7):
            a.append(int(x[j]))
    for i in range(0,len(a),7):##make a bin list of ascii codes
        d2.append(a[i:i+7])
    return d2

def incrSec():
    sum=1
    w=[]
    for i in range (7):
        wi=random.randrange(sum,(sum+5))
        while not(wi>sum) :
            wi=random.randrange(sum,(sum+5))
        w.append(wi)
        sum+=wi
    return w

def getQnR(w):
    sum=0
    for i in range(len(w)):
        sum+=w[i]
    q=random.randrange(sum,sum*2)
    while not(q>sum):
        q=random.randrange(sum,sum*2)
    r=random.randrange(0,sum)
    while not(gcd(q,r)==1):
        r=random.randrange(0,sum)
    return q,r

def encrypt(r,w,q,a):
    b=[]
    dsum=[]
    for i in range(7):
        temp=(r*w[i])%q
        b.append(int(temp))
    ciphertext=''
    sum=0
    for i in range(len(a)):
        temp=0
        for j in range (len(a[i])):
            sum+=a[i][j]*b[j]
            temp+=a[i][j]*b[j]
        ciphertext=str(sum)
        dsum.append(temp)#not finalised
    return ciphertext,b,dsum

def decrypt(dsum,w):
    deciph=''
    d2=[]
    for i in range(len(dsum)):
        temp=dsum[i]
        dsum[i]=(r1*temp)%q
    for i in dsum:
        cnt=0
        ns=''
        while i>0:
            if i<w[cnt%7]:
                cnt+=1
                ns+='0'
                continue
            elif i>=w[cnt%7]:
                i-=w[cnt%7]
                cnt+=1
                ns+='1'
        ns=ns[::-1]
        d2.append(ns)
    for i in d2:#make binary as decimal and get chr of it
        decimal=int(i, 2)
        deciph+=chr(decimal)
    return deciph

def findQ(b):
    qlist=[]
    for i in range (1,6):
         for j in range (2,11):
             for h in range (300,3500):#estimated guess to narrow results
                if b[0]*j%h == b[1]*i%h:
                    if h not in qlist:
                        qlist.append(h)#bruteforce all possible Qs
    return qlist

def findR(b,qlist):
    rlist=[]
    for i in range (2,30):
        for h in qlist:
            r2=b[0]/i%h
            if r2 not in rlist:
                rlist.append(r2)
            break
    return rlist

def breakMH(qlist,rlist):
    pass


#MAIN
if __name__=="__main__":
    plaintext = raw_input("Enter Text You want to ENCRYPT:\t")
    a = bitSeq(plaintext)
    w = incrSec()
    q,r = getQnR(w)
    r1=mod_inverse(r,q)
    ciphertext,b,dsum = encrypt(r,w,q,a)
    sum=int(ciphertext)
    w.sort(reverse=True)
    deciph=decrypt(dsum,w)
    print "plaintext: " + plaintext + "\n" + "ciphertext: " + ciphertext + "\n" +"deciphered: " + deciph

    # ##Attack, while having only b find q and w1 w2

    w.sort()
    qlist=findQ(b)
    rlist=findR(b,qlist)

    # print w[0],w[1],q
    if q in qlist:
        print "True",q
    else: print q
    if q in qlist and r in rlist:
        print "DONE",r,q
