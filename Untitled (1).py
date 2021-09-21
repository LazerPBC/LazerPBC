#!/usr/bin/env python
# coding: utf-8

# In[3]:


from numpy import *
from random import *
from math import *
import matplotlib.pyplot as plt
import time

################## define checking parameter #################

#function calculated minimum P parameter for each initial loading condition
def minsp(s,an):
    #loading site array
    la = []
    def pa(tp,rp,s,a):
        c = (s-1)/2
        p = 0
        ad = a.copy()
        if rp in ad:
            ad.remove(rp)
        aa = array(ad+tp)
        for i in aa:
            p += sqrt((i[0]-c)**2+(i[1]-c)**2)
        return p
    
    if s%2 == 0:
        #define center traps (begin with 2x2)
        #define the center position
        c = [ceil(s/2)-1,ceil(s/2)-1]
        print(c)
        cp = c[0]
        #center fill        
        la.extend([[cp,cp],[cp+1,cp],[cp,cp+1],[cp+1,cp+1]])

        #define layer
        for i in arange(int(1),int(round(s/2))):
            #add orthogonal axes first 
            #orthogonal axes fill
            la.extend([[cp-i,cp],[cp-i,cp+1],[cp,cp+1+i],[cp+1,cp+1+i],[cp+1+i,cp+1],[cp+1+i,cp],[cp+1,cp-i],[cp,cp-i]])

            #add off-orthogonal element
            for k in arange(1,i+1):
                if k != i:
                #non-corner case
                    la.extend([[cp-i,cp-k],[cp-i,cp+1+k],[cp-k,cp+1+i],[cp+1+k,cp+1+i],[cp+1+i,cp+1+k],[cp+1+i,cp-k],[cp+1+k,cp-i],[cp-k,cp-i]])
    
                else:
                    la.extend([[cp-k,cp-k],[cp+1+k,cp+1+k],[cp-k,cp+1+k],[cp+1+k,cp-k]])
    else:
        #define center traps (begin with 2x2)
        #define the center position
        c = [floor(s/2),floor(s/2)]
        cp = c[0]
        #center fill
        la.append([cp,cp])
        
        #define layer
        for i in arange(int(1),int(floor(s/2))+1):
            
            #add orthogonal axes first 
            la.extend([[cp-i,cp],[cp,cp+i],[cp+i,cp],[cp,cp-i]])
    
            #check off-orthogonal element
            for k in arange(1,i+1):
    
                if k != i:
                #non-corner case
                    la.extend([[cp-i,cp-k],[cp-i,cp+k],[cp-k,cp+i],[cp+k,cp+i],[cp+i,cp+k],[cp+i,cp-k],[cp+k,cp-i],[cp-k,cp-i]])    
                else:
                    la.extend([[cp-k,cp-k],[cp+k,cp+k],[cp-k,cp+k],[cp+k,cp-k]])
    # print(len(la))
    lt = la.copy()
    for i in arange(an,s**2):
        # print(i)
        la.remove(lt[i])
    laa = array(la)
    plt.figure()
    plt.plot(laa[:,0],laa[:,1],'o')
    return pa([],[],s,la),la

#system p parameter calculation
def pa(tp,rp,s,a):
    c = (s-1)/2
    p = 0
    ad = a.copy()
    if rp in ad:
        ad.remove(rp)
    aa = array(ad+tp)
    for i in aa:
        p += sqrt((i[0]-c)**2+(i[1]-c)**2)
    return p


#define check neighbour traps function returning the reservoir position
def chn(tp,s,a):
    t = []
    for i in [[tp[0]-1,tp[1]],[tp[0],tp[1]+1],[tp[0]+1,tp[1]],[tp[0],tp[1]-1]]:
        if i in a:
            t.append(i)
    paa = []
    
    #in case that there is no i in a, the loop will not iterate and the op would be NaN
    def pa(tp,rp,s,a):
        c = (s-1)/2
        p = 0
        ad = a.copy()
        if rp in ad:
            ad.remove(rp)
        aa = array(ad+tp)
        for i in aa:
            p += sqrt((i[0]-c)**2+(i[1]-c)**2)
        return p
    for i in t:
        # print('t=',i,'cp=',pa([tp],i,s,a))
        paa.append(pa([tp],i,s,a))
    cp = pa([],[],s,a)
    # print('cp=',cp)
    op = [-1,-1]
    ap =[]
    
    for i in range(len(paa)):
        if paa[i] == min(paa):
            ap.append(i)
    if ap != []:
        if paa[ap[0]] < cp:
            op = (t[choice(ap)]) 
            
    # for i in range(len(paa)): 
    #     # print(paa[i])
    #     if paa[i] < cp:
    #         cp = paa[i]
    #         op.append(t[i])
            
    return op   
############### START Rearranging function #####################
def pm(s,itd):
    
    st = time.time()
    #matching array
    m = []
    
    if s%2 == 0:
        #define center traps (begin with 2x2)
        #define the center position
        c = [ceil(s/2)-1,ceil(s/2)-1]
        cp = c[0]
        ip = [[cp,cp],[cp+1,cp],[cp,cp+1],[cp+1,cp+1]]
        #center fill
        for i in ip:
            # print(i)
            if i in itd:
                m.append([i,i])
                itd.remove(i)
            else: 
                rp = chn(i,s,itd)
                m.append([rp,i])
                if rp in itd:
                    itd.remove(rp)
    
        #define layer
        for i in arange(int(1),int(round(s/2))):
            
            #check orthogonal axes first 
            np = [[cp-i,cp],[cp-i,cp+1],[cp,cp+1+i],[cp+1,cp+1+i],[cp+1+i,cp+1],[cp+1+i,cp],[cp+1,cp-i],[cp,cp-i]]
    
            #orthogonal axes fill
            for j in np:
                if j in itd:
                    m.append([j,j])
                    itd.remove(j)
                else: 
                    rp = chn(j,s,itd)
                    m.append([rp,j])
                    if rp in itd:
                        itd.remove(rp)
    
            #check off-orthogonal element
            for k in arange(1,i+1):
    
                if k != i:
                #non-corner case
                    np = [[cp-i,cp-k],[cp-i,cp+1+k],[cp-k,cp+1+i],[cp+1+k,cp+1+i],[cp+1+i,cp+1+k],[cp+1+i,cp-k],[cp+1+k,cp-i],[cp-k,cp-i]]
                
                #off-orthogonal axes fill
                    for j in np:
                        if j in itd:
                            m.append([j,j])
                            itd.remove(j)
                        else: 
                            rp = chn(j,s,itd)
                            m.append([rp,j])
                            if rp in itd:
                                itd.remove(rp)
    
                else:
                    lp = [[cp-k,cp-k],[cp+1+k,cp+1+k],[cp-k,cp+1+k],[cp+1+k,cp-k]]
                    
                #off-orthogonal axes(corner) fill
                    for j in lp:
                        if j in itd:
                            m.append([j,j])
                            itd.remove(j)
                        else: 
                            rp = chn(j,s,itd)
                            m.append([rp,j])
                            if rp in itd:
                                itd.remove(rp)

    else:
        #define center traps (begin with 2x2)
        #define the center position
        c = [floor(s/2),floor(s/2)]
        cp = c[0]
        ip = [[cp,cp]]
        #center fill
        for i in ip:
            # print(i)
            if i in itd:
                m.append([i,i])
                itd.remove(i)
            else: 
                rp = chn(i,s,itd)
                m.append([rp,i])
                if rp in itd:
                    itd.remove(rp)
    
        #define layer
        for i in arange(int(1),int(floor(s/2))+1):
            
            #check orthogonal axes first 
            np = [[cp-i,cp],[cp,cp+i],[cp+i,cp],[cp,cp-i]]
    
            #orthogonal axes fill
            for j in np:
                if j in itd:
                    m.append([j,j])
                    itd.remove(j)
                else: 
                    rp = chn(j,s,itd)
                    m.append([rp,j])
                    if rp in itd:
                        itd.remove(rp)
    
            #check off-orthogonal element
            for k in arange(1,i+1):
    
                if k != i:
                #non-corner case
                    np = [[cp-i,cp-k],[cp-i,cp+k],[cp-k,cp+i],[cp+k,cp+i],[cp+i,cp+k],[cp+i,cp-k],[cp+k,cp-i],[cp-k,cp-i]]
                
                #off-orthogonal axes fill
                    for j in np:
                        if j in itd:
                            m.append([j,j])
                            itd.remove(j)
                        else: 
                            rp = chn(j,s,itd)
                            m.append([rp,j])
                            if rp in itd:
                                itd.remove(rp)
    
                else:
                    lp = [[cp-k,cp-k],[cp+k,cp+k],[cp-k,cp+k],[cp+k,cp-k]]
                    
                #off-orthogonal axes(corner) fill
                    for j in lp:
                        if j in itd:
                            m.append([j,j])
                            itd.remove(j)
                        else: 
                            rp = chn(j,s,itd)
                            m.append([rp,j])
                            if rp in itd:
                                itd.remove(rp)
        
    et = time.time()
    
    
    #layer mod alg
    xi = []
    yi = []
    xf = []
    yf = []                        
    unf = 0
    mc = 0
    ep = 0
    
    
    xfi = []
    yfi = []
    xe = []
    ye = []
    iitd = []
    for i in m:
        xf.append(i[0][0])
        yf.append(i[0][1])
        xi.append(i[1][0])
        yi.append(i[1][1])
        if i[0][0] == -1:
            unf += 1
            xe.append(i[1][0])
            ye.append(i[1][1])
        else:
            xfi.append(i[1][0])
            yfi.append(i[1][1])
            iitd.append(i[1])
            if i[0]!=i[1]:
                mc+=1
    
    fillfrac = 1-unf/((s)**2)
    # plt.figure()
    # plt.plot(xi,yi,'ro')
    # plt.plot(xf,yf,'b+')          
    print('filfrac = ',fillfrac,',  No. of moves=',mc,'no. of moves + vacancies',mc+unf)
    plt.figure()
    plt.plot(xfi,yfi,'o')
    plt.plot(xe,ye,'r+')
    
    
    
    return m,iitd,pa([],[],s,iitd),et-st,mc

############### END Rearranging function #####################
        
#loading site's size
s = 20

#array containing occupied trap position
ot = []
it = []

#occupying parameter array
oa = zeros((s,s))



#generating random occupied traps
for i in range(s*s):
    r = randrange(10)
    if r >= 5:
#set the index to start at 0 position to make the following xy position converting
        ot.append(i)
        it.append([i%s,trunc(i/s)])
        oa[int(i%s)][int(trunc(i/s))] = 1
        # da[int(i%s)][int(trunc(i/s))] += 1
        



minp = minsp(s,len(it))[0]
print('minimum system s P=', minp)
#Plot initial loaded traps
it = array(it)
plt.figure()
plt.plot(it[:,0],it[:,1],'o') 



#convert 'it' to list for element checking
itl = it.tolist()
itd = itl.copy()


cmp = []
ctim = []
Nom = []
cmp.append(pa([],[],s,itd))

itn = 10

for i in range(itn):
# dummy = 100000
# while dummy > pm(s,itd)[2]:  
    gd = pm(s,itd)
    itd = gd[1]
    # dummy = gd[2]
    cmp.append(gd[2])
    ctim.append(gd[3])
    Nom.append(gd[4])

    
#accNOM
aNom = []
for i  in range(len(Nom)):
    aNom.append(sum(Nom[0:i+1]))


plt.figure()
plt.plot(cmp,'*',label="P value for each iteration")
plt.plot([0,itn],[minp,minp], label='minimum system s P')
plt.text(4, max(cmp)-10, 'minimum system s P=%.3f'%(minp))
plt.text(4, max(cmp)-15, 'minimum P from iteration=%.3f'%(min(cmp)))

plt.figure()
plt.plot(Nom,'+')

plt.figure()
plt.plot(aNom,'h')
plt.xlabel('iterations')
plt.ylabel('accumulated number of moves')

plt.figure()
plt.plot(Nom,array(cmp[1:len(cmp)])-array(cmp[0:len(cmp)-1]),'^')
plt.ylabel('inversed compactness')
plt.xlabel('Number of moves')

plt.figure()
plt.plot(aNom,array(cmp[1:len(cmp)])-array(cmp[0:len(cmp)-1]),'^')
plt.ylabel('inversed compactness')
plt.xlabel('accumulative number of moves')

print('calculation time for each iteration',ctim)
print('total calculation time', sum(ctim))



# In[2]:


from numpy import *
from random import *
from math import *
import matplotlib.pyplot as plt
import time


# In[ ]:





# In[ ]:




