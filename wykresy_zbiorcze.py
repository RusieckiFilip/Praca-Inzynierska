# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 19:49:14 2022

@author: Filip
"""


import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
import pandas as pd
import seaborn as sns
import scipy
import re 
from matplotlib.lines import Line2D
import pylab as plt
import scipy.optimize as op



####### ZBIORCZY ###########

dane_f1 =  pd.read_csv("https://raw.githubusercontent.com/RusieckiFilip/PracaInz/main/zbiorczy_f1.csv", sep = ";")
dane_f08 =  pd.read_csv("https://raw.githubusercontent.com/RusieckiFilip/PracaInz/main/zbiorczy_f08.csv", sep = ";")
dane_f16 =  pd.read_csv("https://raw.githubusercontent.com/RusieckiFilip/PracaInz/main/zbiorczy_f16.csv", sep = ";")
dane_f128 =  pd.read_csv("https://raw.githubusercontent.com/RusieckiFilip/PracaInz/main/zbiorczy_f128.csv", sep = ";")

dane_f08 = dane_f08.append({'predkosc':606.9,'ITD.':12,'kat':0,'Cisnienie': 3.3},ignore_index=True)
dane_f08 = dane_f08.append({'predkosc':565,'ITD.':2758,'kat':2,'Cisnienie': 1.9},ignore_index=True)


######### zmienianie kategorii na opozniony i szybki

for i, j in zip(dane_f1["ITD."], range(len(dane_f1["ITD."]))):
    if i > 3 and i <= 100:
        dane_f1["kat"][j]=0
for i, j in zip(dane_f08["ITD."], range(len(dane_f08["kat"]))):
    if i > 3 and i <= 100:
        dane_f08["kat"][j]=0
for i, j in zip(dane_f16["ITD."], range(len(dane_f16["kat"]))):
    if i > 3 and i <= 100:
        dane_f16["kat"][j]=0
for i, j in zip(dane_f128["ITD."], range(len(dane_f128["kat"]))):
    if i > 11 and i <= 100:
        dane_f128["kat"][j]=0

M_1 = 407.3
M_08 = 395.8
M_16 = 437.7    
M_128 = 422.3

w = 0.4    # bar width
x = [1,2,3,4] # x-coordinates of your bars
colors = [(0, 0, 1, 1), (1, 0, 0, 1),"k", '#04FF03']    # corresponding colors
y = [dane_f1["ITD."],dane_f08["ITD."],dane_f16["ITD."],dane_f128["ITD."]]



fig, ax = plt.subplots()


    
fig.suptitle('Opoznienie zaplonu od stezenia mieszaniny', fontsize=23)
    
plt.style.use('seaborn-deep')
plt.xlabel("Wspolczynik ekwiwalencji", fontsize=17)
plt.ylabel("Opoznienie zaplonu [us]", fontsize=17)
plt.grid(color='#717171', linestyle='--', linewidth=0.3)
plt.yscale("log")
    
plt.tick_params(axis='both', labelsize=16)

ax.bar(x,
       height=100,
       yerr=100,    # error bars
       capsize=0, # error bar cap width in points
       width=0,    # bar width
       tick_label=["fi=0,8","fi=1","fi=1,28","fi=1,6"],
       color=(0,0,0,0),  # face color transparent
       edgecolor=(0,0,0,0),
       #ecolor=colors,    # error bar colors; setting this raises an error for whatever reason.
       )
#### tworzenie markow #####
mark1=[]
mark08=[]
mark16=[]
mark128=[]

dane_f1["Mach"] = dane_f1["predkosc"]/M_1 
dane_f08["Mach"] = dane_f08["predkosc"]/M_08 
dane_f16["Mach"] = dane_f16["predkosc"]/M_16
dane_f128["Mach"] = dane_f128["predkosc"]/M_128 

for i in range(len(dane_f1["ITD."])):
    if dane_f1["kat"][i]==0: mark1.append("d")
    elif dane_f1["kat"][i]==1: mark1.append((5, 1))
    elif dane_f1["kat"][i]==2: mark1.append("o")
    elif dane_f1["kat"][i]==3: mark1.append("s")
    elif dane_f1["kat"][i]==4: mark1.append("^")
    
for i in range(len(dane_f08["ITD."])):
    if dane_f08["kat"][i]==0: mark08.append("d")
    elif dane_f08["kat"][i]==1: mark08.append((5, 1))
    elif dane_f08["kat"][i]==2: mark08.append("o")
    elif dane_f08["kat"][i]==3: mark08.append("s")
    elif dane_f08["kat"][i]==4: mark08.append("^")
    
for i in range(len(dane_f16["ITD."])):
    if dane_f16["kat"][i]==0: mark16.append("d")
    elif dane_f16["kat"][i]==1: mark16.append((5, 1))
    elif dane_f16["kat"][i]==2: mark16.append("o")
    elif dane_f16["kat"][i]==3: mark16.append("s")
    elif dane_f16["kat"][i]==4: mark16.append("^")
    
for i in range(len(dane_f128["ITD."])):
    if dane_f128["kat"][i]==0: mark128.append("d")
    elif dane_f128["kat"][i]==1: mark128.append((5, 1))
    elif dane_f128["kat"][i]==2: mark128.append("o")
    elif dane_f128["kat"][i]==3: mark128.append("s")
    elif dane_f128["kat"][i]==4: mark128.append("^")
    
custom_marks = [Line2D([0], [0], marker='d', color='w', label='Szybki zaplon',
                          markerfacecolor='k', markersize=17),        
                Line2D([0], [0], marker='o', color='w', label='Pozny zaplon',
                          markerfacecolor='k', markersize=17),
                Line2D([0], [0], marker=(5, 1), color='w', label='Detonacja na narozu',
                          markerfacecolor='k', markersize=19),
                Line2D([0], [0], marker='^', color='w', label='Opozniona detonacja',
                          markerfacecolor='k', markersize=17),
                Line2D([0], [0], marker='s', color='w', label='Przedwczesna detonacja',
                          markerfacecolor='k', markersize=17)]

# fi = 08
for i, m, y_ in zip(range(len(mark08)), mark08, dane_f08["ITD."]) :
    # distribute scatter randomly across whole width of bar
    ax.scatter(x[0] + np.random.random(y[1].size)[i] * w - w / 2, y_, color=colors[1], marker=m, s = 800, alpha=0.5)
    
# fi = 1
for i, m, y_ in zip(range(len(mark1)), mark1, dane_f1["ITD."]) :
    # distribute scatter randomly across whole width of bar
    ax.scatter(x[1] + np.random.random(y[0].size)[i] * w - w / 2, y_, color=colors[0], marker=m, s = 800, alpha=0.5)

# fi = 128
for i, m, y_ in zip(range(len(mark128)), mark128, dane_f128["ITD."]) :
    # distribute scatter randomly across whole width of bar
    ax.scatter(x[2] + np.random.random(y[3].size)[i] * w - w / 2, y_, color=colors[3], marker=m, s = 800, alpha=0.5)

# fi = 16
for i, m, y_ in zip(range(len(mark16)), mark16, dane_f16["ITD."]) :
    # distribute scatter randomly across whole width of bar
    ax.scatter(x[3] + np.random.random(y[2].size)[i] * w - w / 2, y_, color=colors[2], marker=m, s = 800, alpha=0.5)


plt.legend(handles = custom_marks,fontsize=19, loc="upper center")
plt.tight_layout()




  ########################## WYKRES ITD i CISNIENIA OD PREDKOSCI #################################
def pred(dane_f1, fi,dg,gg):
    fig1 = plt.figure("IDT(V) "+fi,figsize=(16, 9), dpi=150)
    plt.clf()
        
    fig1.suptitle("IDT(V) " + fi, fontsize=17)
        
    
    plt.style.use('seaborn-deep')
    plt.xlabel("Predkosc [m/s]", fontsize=13)
    plt.ylabel("IDT [us]", fontsize=13)
    plt.grid(color='#717171', linestyle='--', linewidth=0.3)
    #plt.ylim(0,2.5)
    #plt.xlim(2000,12000)
    plt.scatter(dane_f1["predkosc"],dane_f1["ITD."])
    plt.yscale("log")
    plt.xlim(dg,gg)
    
    
    #plt.legend(loc="upper left", fontsize=11)
    plt.tick_params(axis='both', labelsize=12)
        
    fig1.tight_layout()

pred1 = pred(dane_f1,"fi = 1",600,950)
pred2 = pred(dane_f08,"fi = 0,8",550,650)
pred3 = pred(dane_f16,"fi = 1,6",620,750)
pred4 = pred(dane_f128,"fi = 1,28",600,900)



fig1 = plt.figure("IDT(V)",figsize=(16, 9), dpi=150)
plt.clf()
        
fig1.suptitle("IDT(V)", fontsize=17)
        
    
plt.style.use('seaborn-deep')
plt.xlabel("Predkosc [m/s]", fontsize=13)
plt.ylabel("IDT [us]", fontsize=13)
plt.grid(color='#717171', linestyle='--', linewidth=0.3)

plt.scatter(dane_f1["predkosc"],dane_f1["ITD."], c=(0, 0, 1, 1), label = "fi = 1")
plt.scatter(dane_f08["predkosc"],dane_f08["ITD."], c=(1, 0, 0, 1), label = "fi = 0,8")
plt.scatter(dane_f16["predkosc"],dane_f16["ITD."], c='k', label = "fi = 1,6")
plt.scatter(dane_f128["predkosc"],dane_f128["ITD."], c='#04FF03', label = "fi = 1,28")

plt.plot([623.4,757.6],[3.808,26.3], linestyle='-.', color = "r", linewidth=1.3, alpha=0.8)
plt.plot([725,850],[2.5,2.5], linestyle='-.', color = "r", linewidth=1.3, alpha=0.8)
plt.plot([560,735],[100,100], linestyle='-.', color = "r", linewidth=1.3, alpha=0.8)

plt.text(750,10,"Opozniona detonacja", fontsize = 15)
plt.text(875,1.8,"Detonacja w narozu", fontsize = 15)
plt.text(725,55,"Szybki zaplon", fontsize = 15)
plt.text(725,350,"Pozny zaplon", fontsize = 15)

plt.yscale("log")
plt.xlim(550,950)
    
    
plt.legend(loc="upper right", fontsize=11)
plt.tick_params(axis='both', labelsize=12)
        
fig1.tight_layout()





k1 = dane_f1[dane_f1["kat"] != 3][:]
k16 = dane_f16[dane_f16["kat"] != 3][:]
k08 = dane_f08[dane_f08["kat"] != 3][:]




fig2 = plt.figure("IDT(p)",figsize=(16, 9), dpi=150)
plt.clf()
        
fig2.suptitle("IDT(p)", fontsize=17)
        
    
plt.style.use('seaborn-deep')
plt.xlabel("Cisnienie [MPa]", fontsize=13)
plt.ylabel("IDT [us]", fontsize=13)
plt.grid(color='#717171', linestyle='--', linewidth=0.3)

plt.scatter(k1["Cisnienie"],k1["ITD."], c=(0, 0, 1, 1), label = "fi = 1")
plt.scatter(k08["Cisnienie"],k08["ITD."], c=(1, 0, 0, 1), label = "fi = 0,8")
plt.scatter(k16["Cisnienie"],k16["ITD."], c='k', label = "fi = 1,6")
plt.scatter(dane_f128["Cisnienie"],dane_f128["ITD."], c='#04FF03', label = "fi = 1,28")



plt.plot([10.2,10.2],[0.8,160], linestyle='-.', color = "r", linewidth=1.3, alpha=0.8)


plt.text(10.6,85,"Zakres detonacji", fontsize = 17)
plt.text(3.35,85,"Zakres deflagracji", fontsize = 17)

plt.yscale("log")
#plt.xlim(550,950)
    
    
plt.legend(loc="upper right", fontsize=11)
plt.tick_params(axis='both', labelsize=12)
        
fig2.tight_layout()




##########################################
kopia = pd.concat([dane_f1[:],dane_f08[:],dane_f16[:],dane_f128[:]], ignore_index=True) 

kopia = kopia.drop(index=[11,16,22], axis=0)
kopia = kopia.dropna()

# #polynomial fit with degree = 2
# model = np.poly1d(np.polyfit(kopia['Mach'], kopia['Cisnienie'], 1))

# #add fitted polynomial line to scatterplot
# polyline = np.linspace(1, 60, 50)

def exp_fit(x,a,b,c):
    y = a*np.exp(b*x)+c
    return y


fit = op.curve_fit(exp_fit,kopia['Mach'], kopia['Cisnienie'])
fit_eq = fit[0][0]*np.exp(fit[0][1]*kopia['Mach'])+fit[0][2]

df = pd.DataFrame(columns = ["Mach","Dopasowanie"])
df["Mach"] = kopia["Mach"]
df["Dopasowanie"] = fit_eq

df = df.sort_values(by="Mach",ignore_index=True)
##########################################

fig3 = plt.figure("p(M)",figsize=(16, 9), dpi=150)
plt.clf()
        
fig3.suptitle("p(M)", fontsize=17)
        
    
plt.style.use('seaborn-deep')
plt.xlabel("Mach [-]", fontsize=13)
plt.ylabel('$\Delta p\ [MPa]$', fontsize=13)
plt.grid(color='#717171', linestyle='--', linewidth=0.3)

plt.scatter(dane_f1["Mach"],dane_f1["Cisnienie"]-0.1, c=(0, 0, 1, 1), label = "fi = 1")
plt.scatter(dane_f08["Mach"],dane_f08["Cisnienie"]-0.1, c=(1, 0, 0, 1), label = "fi = 0,8")
plt.scatter(dane_f16["Mach"],dane_f16["Cisnienie"]-0.1, c='k', label = "fi = 1,6")
plt.scatter(dane_f128["Mach"],dane_f128["Cisnienie"]-0.1, c='#04FF03', label = "fi = 1,28")
plt.plot(df["Mach"],df["Dopasowanie"])
plt.text(1.8,16,r'$0.225 \cdot e^{2.24x}-4.4$', fontsize=15)

#plt.plot(polyline, model(polyline))

plt.xlim(1.25,2.2)
    
    
plt.legend(loc="best", fontsize=11)
plt.tick_params(axis='both', labelsize=12)
        
fig3.tight_layout()





