# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 13:34:00 2022

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





############ WCZYTANIE DANYCH O CZUJNIKACH ######################################################


xxx = pd.read_csv("https://raw.githubusercontent.com/RusieckiFilip/PracaInz/main/VMPA.csv", sep = ";")

for i in xxx["SN"]:
    if type(i)==int:
        i = str(i)
        
####### FUNKCJA WCZYTANIA DANYCH ###############################################################################

def wczytanie_danych(nazwa_pliku, nazwa_folderu, kanal=0):
    data = pd.read_csv("https://raw.githubusercontent.com/RusieckiFilip/PracaInz/main/"+
                       nazwa_folderu+"/H2-pow_fi1/"+nazwa_pliku, sep = "\t")
    
    #### USUWANIE SZUMU ######
    if kanal != 0:
        i=0
        for j in data[kanal]:
            if data[kanal][i] > 0.45:
                data[kanal] = data[kanal].drop(labels=list(range(i,15998)), axis=0)    
                break
            i+=1
        for i in data:
            j=0
            for k in data[i]:
                if i != "time [us]" and j < 2000:
                    data[i][j]=0
                else: break
                j+=1
    return data


############# WCZYTANIE DANYCH ##########################################################################################################################


data21 = wczytanie_danych("test2.csv","TESTY-H2-pow_fi08_101121","ch 3")
text21 = wczytanie_danych("test2_t.csv","TESTY-H2-pow_fi08_101121")

data22 = wczytanie_danych("test3.csv","TESTY-H2-pow_fi08_101121","ch 3")
text22 = wczytanie_danych("test3_t.csv","TESTY-H2-pow_fi08_101121")

data23 = wczytanie_danych("test4.csv","TESTY-H2-pow_fi08_101121","ch 3")
text23 = wczytanie_danych("test4_t.csv","TESTY-H2-pow_fi08_101121")



############ FUNKCJA TWORZACA WYKRESY ######################################################

####### Funkcja(dane z czujnikow, opis, numer exp, trigger dla SN, trigger dla SN powrotna fala, trigger dla SJ, trig dla 2 pierwszych SN, czas po ktorym mierzymy trigger powrotnej fali, max dopusz predkosc fizyczna) 

def funkcja(data1,text1,numer,tr_SN, tr_SN_f2, tr_SJ, tr_SN2, czas_zbior, V_max, V_CJ, aP, t_d,tak):
    
    ######## TWORZENIE KOPII #########
    data = data1[:]

    ######## Obliczanie TOA_P dla kanałow bez sond jonizacyjnych ##########################
    
    temp = []
    l = -1
    for i in data1:
        if i != "time [us]" and l < 2:
            k = -1
            for j in data1[i]:
                k += 1
                if data1[i][k] > tr_SN2:
                    temp.append(data1["time [us]"][k]/1000)
                    break
        l += 1
    
    ######################################################################################
    
    
    
    list1=[]
    for i in text1["Tabela"]:
        l=0
        for j in xxx["SN"]:
            if j in i:
                print("Czujnik: ", j)
                list1.append(xxx["VMPA"][l])
            l+=1
   
    ############## Pobieranie wspolrzednych i opisow ######################################
    pattern = "\](.*?)\["
    list2=[]
    print("\n")
    l=0
    
    # Zczytanie pozycji z czujnika
    for i in text1["Tabela"]:
        if  i != "time [us]":
            if "POS" in i:
                substring = re.search(pattern, i).group(1)
                list2.append(float(substring))
    
    # Zczytanie opisu eksperymentu
    for i in text1["Tabela"]:
        if  i != "time [us]":
            if "[EXP_DESC_s]" in i:
                opis = i
                break
            
    for i in text1["Tabela"]:
        if  i != "time [us]":
            if "/EXP_DESC_s" in i:
                opis = opis + " " + i
                break
    opis = re.search(pattern, opis).group(1)
        
    ############ TWORZENIE DATAFRAME Z DANYMI CZUJNIKOW ####################################
    d = {'Kanal': range(1,9), 'VPMA': list1, "Odleglosc": list2[:8]}
    df1 = pd.DataFrame(data=d)
    
    l=-1
    
    ########## PRZELICZENIE NA MPa CZUJNIKOW ###########
    for i in data1:
        if  i != "time [us]" and l < 8:
            data1[i] = data1[i]/df1["VPMA"][l]+0.1
        l+=1
        if tak == 1:
            if l>8 and l<12:
                data1[i] = data1[i]*1.7
    #####################################################
    

    
    ########################## WYKRES ODCZYTÓW CZUJNIKÓW #################################
        
        
    fig1 = plt.figure("data" + numer,figsize=(16, 9), dpi=150)
    plt.clf()
    
    fig1.suptitle(opis, fontsize=20)
    
    ax1=plt.subplot(211)
    plt.style.use('seaborn-deep')
    plt.xlabel("Czas [us]", fontsize=15)
    plt.ylabel("P [MPa]", fontsize=15)
    plt.grid(color='#717171', linestyle='--', linewidth=0.3)
    #plt.ylim(0,1)
    plt.xlim(2000,t_d)
    color = cm.rainbow(np.linspace(0, 1, 8))
    for i,c in zip(range(1,9),color):
        plt.plot(data1["time [us]"],data1["ch "+ str(i)], linewidth=1.5, label =  "ch"+ str(i) + " SN", c=c)
    plt.legend(loc="upper left", fontsize=11)
    plt.tick_params(axis='both', labelsize=14)
        
    ax1=plt.subplot(212)
    plt.style.use('seaborn-deep')
    plt.xlabel("Czas [us]", fontsize=15)
    plt.ylabel("U [V]", fontsize=15)
    plt.grid(color='#717171', linestyle='--', linewidth=0.3)
    plt.ylim(0,1)
    plt.xlim(2000,t_d)
    for i in range(1,15):
        if i > 8:
            plt.plot(data1["time [us]"],data1["ch "+ str(i)], linewidth=1.5, label =  "ch"+ str(i) + " SJ", c=color[i-7] )
    plt.legend(loc="upper left", fontsize=11)
    plt.tick_params(axis='both', labelsize=14)
    
    fig1.tight_layout()
    
    list3=temp
    list4=[0.1,4]
    l=-1
    
        ################ WYKRES ZBIORCZY ####################
    
    fig4 = plt.figure("Zbiorczy" + numer,figsize=(16, 9), dpi=150)
    plt.clf()
    
    fig4.suptitle(opis, fontsize=20)
    zbiorczy = plt.subplot(111)
    
    plt.style.use('seaborn-deep')
    plt.xlabel("Czas [us]", fontsize=15)
    plt.ylabel("P[MPa] + x[m]", fontsize=15)
    plt.grid(color='#717171', linestyle='--', linewidth=0.3)
    #plt.ylim(0,2.5)
    plt.xlim(2000,t_d)
    color = cm.rainbow(np.linspace(0, 1, 8))
    for i, c in zip(range(1,9),color):
        plt.plot(data1["time [us]"],data1["ch "+ str(i)] + df1["Odleglosc"][i-1], 
                 linewidth=1, label = "ch"+ str(i) + " SN, " + str(df1["Odleglosc"][i-1])+" m", c=c)
    plt.tick_params(axis='both', labelsize=14)
    plt.legend(loc="upper left", fontsize=13)
    plt.tight_layout()
    
    
    
    ###### USUWANIE kanałow bez sond jonizacyjnych #################################
    
    data1.drop('ch 1',
      axis='columns', inplace=True)
    data1.drop('ch 2',
      axis='columns', inplace=True)
    
    ################### USTALENIE KIEDY DOTARL PLOMIEN I FALA DO CZUJNIKOW  ###################
    
    for i in data1:
        if  i != "time [us]" and l < 6:
            k=-1
            for j in data1[i]:
                k+=1
                if data1[i][k] > tr_SN:
                    list3.append(data1["time [us]"][k]/1000)
                    break
        elif i != "time [us]":
            k=-1
            for j in data1[i]:
                k+=1
                if data1[i][k] > tr_SJ:
                    list4.append(data1["time [us]"][k]/1000)
                    break
        l+=1
    
    list4[1]=list4[2]*list2[1]/list2[2]
    df1["TOA_P [ms]"]=list3
    df1["TOA_V [ms]"]=list4
    
    ######################### WYKRES TOA ####################################################
    
    fig2 = plt.figure("TOA" + str(numer),figsize=(16, 9), dpi=150)
    plt.clf()
    
    fig2.suptitle('ToA\n' + opis, fontsize=20)
    
    plt.style.use('seaborn-deep')
    plt.xlabel("Dystans [m]", fontsize=15)
    plt.ylabel("Czas [ms]", fontsize=15)
    plt.grid(color='#717171', linestyle='--', linewidth=0.3)
    plt.xlim(0,3)
    plt.tick_params(axis='both', labelsize=14)
    
    
    plt.plot([0,df1["Odleglosc"][0]],[0,df1["TOA_P [ms]"][0]], linestyle='--', color="g")
    plt.plot([0,df1["Odleglosc"][2]],[0,df1["TOA_V [ms]"][2]], linestyle='--', color="b")
    
    
    plt.plot(df1["Odleglosc"],df1["TOA_P [ms]"], color="g", label="Fala cisnieniowa",marker="o")
    plt.plot(df1["Odleglosc"][2:],df1["TOA_V [ms]"][2:], color="b", label="Front plomienia",marker="o")
    plt.legend(fontsize=15, loc="upper left")
    plt.tight_layout()
    
    
    ################ SREDNIA ODLEGLOSC POMIEDZY CZUJNIKAMI #########################
    
    list5=[0]
    l=1
    for i in df1["Odleglosc"]:
        if l<8:
            list5.append((df1["Odleglosc"][l]+df1["Odleglosc"][l-1])/2)
        l+=1
    df1["Srednia odleglosc"]=list5
    
    
    ################### PREDKOSC FALI CISNIENIOWEJ ###########################
    
    list6=[0]
    l=1
    print("\nEksperyment: "+numer)
    for i in df1["TOA_P [ms]"]:
        if l<8:
            if (df1["Odleglosc"][l]-df1["Odleglosc"][l-1])/(df1["TOA_P [ms]"][l]-df1["TOA_P [ms]"][l-1])>100:
                list6.append(0)
            else: 
                list6.append((df1["Odleglosc"][l]-df1["Odleglosc"][l-1])*1000/(df1["TOA_P [ms]"][l]-df1["TOA_P [ms]"][l-1]))
                print("Odleglosc "+str(l+1)+" i", str(l),":", df1["Odleglosc"][l],",", df1["Odleglosc"][l-1], ";TOAP1-2:",
                      df1["TOA_P [ms]"][l],",",df1["TOA_P [ms]"][l-1], ", droga: ", round((df1["Odleglosc"][l]-df1["Odleglosc"][l-1]), 3))
            l+=1 
    df1["Predkosc P"]=list6
    
    
    
    ############# PREDKOSC PLOMIENIA #############################
    list7=[0]
    l=1
    for i in df1["TOA_V [ms]"]:
        if l<8:
            if (df1["Odleglosc"][l]-df1["Odleglosc"][l-1])/(df1["TOA_V [ms]"][l]-df1["TOA_V [ms]"][l-1])>100:
                list7.append(0)
            else: 
                list7.append((df1["Odleglosc"][l]-df1["Odleglosc"][l-1])*1000/(df1["TOA_V [ms]"][l]-df1["TOA_V [ms]"][l-1]))
                print("Odleglosc "+str(l+1)+" i", str(l),":",df1["Odleglosc"][l],",",df1["Odleglosc"][l-1], ",TOAV1-2:",
                      df1["TOA_V [ms]"][l],",",df1["TOA_V [ms]"][l-1])
            l+=1
    df1["Predkosc V"]=list7
    
    
    ########## USREDNIANIE ZA DUZYCH WARTOSCI PREDKOSCI ########################
    ########## Error gdy pierwsza lub ostatnia wartosc predkosci wieksza od 1950 lub ujemna
    j=-1
    for p,v in zip(list6,list7):
        j+=1
        if j < 7 and (abs(p) > V_max or (list6[j-1]>0 and list6[j+1]>0 and p < 0) 
                      or (p > 2*(list6[j-1]+list6[j+1])/2 and list6[j-1]>0 and list6[j+1] > 0)  
                      or (p > 2*(abs(list6[j-1])+abs(list6[j+1]))/2) ):
            
            if (list6[j-1]<0 and list6[j+1]<0 and p < 0): list6[j] = ((list6[j-1])+(list6[j+1]))/2
            else: list6[j] = (abs(list6[j-1])+abs(list6[j+1]))/2 
        elif j < 7 and (abs(v) > V_max or (list7[j-1]>0 and list7[j+1]>0 and v < 0) 
                        or (v > 2*(list7[j-1]+list7[j+1])/2 and list7[j-1]>0 and list7[j+1] > 0)  
                        or (v > 2*(abs(list7[j-1])+abs(list7[j+1]))/2) ):
            
            if (list7[j-1]<0 and list7[j+1]<0 and v < 0): list7[j] = ((list7[j-1])+(list7[j+1]))/2 
            else: list7[j] = list7[j] = (abs(list7[j-1])+abs(list7[j+1]))/2
       
    #################
    
        else: ########### USUWAM UJEMNE WARTOSCI ALE CZY POPRAWNIE  ???????   ###########
            list6[j]=abs(list6[j])
            list7[j]=abs(list7[j])
            
    ################
    
    fig3 = plt.figure("V" + numer,figsize=(16, 9), dpi=150)
    plt.clf()
    
    fig3.suptitle('dx/dt\n' + opis + "\n", fontsize=20)
    
    plt.style.use('seaborn-deep')
    plt.xlabel("Dystans [m]", fontsize=15)
    plt.ylabel("Predkosc [m/s]", fontsize=15)
    plt.grid(color='#717171', linestyle='--', linewidth=0.3)
    
    plt.plot([0,list5[1]],[0,df1["Predkosc P"][1]], linestyle='--', color="g")
    plt.plot([0,list5[1]],[0,list7[1]], linestyle='--', color="b")
    
    plt.plot([list5[1],list5[2]],[df1["Predkosc P"][1],list6[2]], color="g",marker="o")
    plt.plot(list5[2:],list6[2:], label="Fala cisnieniowa", color="g",marker="o")
    plt.plot(list5[1:],list7[1:], label="Front plomienia",  color="b",marker="o")
    plt.ylim(0,V_CJ+200)
    plt.tick_params(axis='both', labelsize=14)
    
    V_CJ_t = str(V_CJ)
    aP_t = str(aP)
    plt.plot([0,3.5], [V_CJ,V_CJ], linestyle='-.', color = "r", linewidth=1.5, alpha=0.6)
    plt.plot([0,3.5], [aP,aP], linestyle='-.', color = "r", linewidth=1.5, alpha=0.6)
    plt.xlim(0,3)
    plt.text(0.1, V_CJ+30, r'$V_{CJ}=\ $'+V_CJ_t+'[m/s]', fontsize=15)
    plt.text(0.1, aP+30, r'$a_{p}=\ $'+aP_t+'[m/s]', fontsize=15)
    
    
    plt.legend(fontsize=15, loc="upper right")
    plt.tight_layout()
    
    
    
    
    

    
    ###### CIAG DALSZY WYKRESU ZBIORCZEGO #####
    
    df_temp = df1
    
    df_temp=df_temp.drop(df_temp.index[2])
    
    
    print("DF TEMP ", df_temp['Odleglosc'])
    
    ##### Linia pochyla reprezentujaca predkosc pierwszej fali #####
    zbiorczy.plot(df_temp["TOA_P [ms]"]*1000, df_temp["Odleglosc"]+0.08,
                  linewidth=2, color='k')
    
    
    ########## NIEDOKONCZONE  ##############################
    
     
    ###### USUWANIE kanału zanieczyszczonego i urwanego #################################
    
    data.drop('ch 3',
      axis='columns', inplace=True)
    
    ################### USTALENIE KIEDY DOTARLA FALA DO CZUJNIKOW  ###################
    l=-1
    list_zbior = []
    list_czas = []
    
    ##### CZAS DOTARCIA POWROTNEJ FALI #######
    for i, o in zip(data,df_temp["Odleglosc"]):
        if  i != "time [us]" and l < 6:
            k=czas_zbior
            print("Kanal ",i)
            for j in data[i]:
                k+=1
                if data[i][k] > tr_SN_f2:
                    list_czas.append(data["time [us]"][k])
                    if data[i][k]> 1.2: list_zbior.append(o+0.3)  #Gdy za duza wartosc
                    else: list_zbior.append(data[i][k-100]+o-0.3)
                    break
        l+=1
     
    list_czas.append(df1["TOA_P [ms]"][7]*1000)
    list_zbior.append(df_temp["Odleglosc"][7]+0.08)
    list_czas = list_czas[:7]
    
    list_czas = list_czas[::-1]

    """
    ####### Wartosci cisnien ToA powrotnej fali #######
    j=0
    for i in df_temp["Odleglosc"]:
        if j < 7: list_zbior.append(i+tr_SN_f2)
        j+=1
    
    """
    list_zbior = list_zbior[::-1]
   
    
    print("List zbior",  list_zbior)
    print("List czas",  list_czas)
   
    ###### Linia pochyla reprezentujaca fale powrotna ########
    war_y  = df_temp["Odleglosc"][::-1]+0.08
    
    zbiorczy.plot(list_czas, war_y,
                  linewidth=2, color='k')
    
    
    ##### OPOZNIONY ZAPLON ########
    predkosc_powrotn = (1000000*(df_temp["Odleglosc"][7]-df_temp["Odleglosc"][6]))/(list_czas[1]-list_czas[0])
    
    opoz_zapl = (df1['TOA_V [ms]'][7]-df1['TOA_P [ms]'][7])*1000
    print("\nOPOZNIENIE ZAPLONU:",opoz_zapl,"[us]\n")
    print("OSTATNIA PREDKOSC:", round(list6[7],1),"[m/s]\n")
    print("PREDKOSC POWROTNA", round(predkosc_powrotn,1), "[m/s]\n")
    
   # for i in data1:
    
    return (df1, opoz_zapl)
    
    




##########################################################################################################

###### WYSWIETLENIE WYKRESOW #############################################################################

####### Funkcja(dane z czujnikow, opis, numer exp, trigger dla SN, trigger dla SN powrotna fala,
####### trigger dla SJ, trig dla 2 pierwszych SN, czas po ktorym mierzymy trigger powrotnej fali, max pred dopuszcz m/s) 

######## TESTY-H2-pow_fi08_101121 #########


df21=funkcja(data21,text21,"21",0.17,0.188,0.09,0.1,4700,1100,1870.7,946.5,13500,0)
df22=funkcja(data22,text22,"22",0.17,0.22,0.2,0.17,9900,1100,1870.7,946.5,13500,0)
df23=funkcja(data23,text23,"23",0.17,0.25,0.098,0.2,9900,1100,1870.7,946.5,13000,0)

####### ZBIORCZY ###########


