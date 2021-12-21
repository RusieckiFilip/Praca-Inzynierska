

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
import pandas as pd
import seaborn as sns
import re 


############ WCZYTANIE DANYCH O CZUJNIKACH ######################################################


xxx = pd.read_csv("https://raw.githubusercontent.com/RusieckiFilip/PracaInz/main/VMPA.csv", sep = ";")

for i in xxx["SN"]:
    if type(i)==int:
        i = str(i)
        
####### FUNKCJA WCZYTANIA DANYCH ###############################################################################

def wczytanie_danych(nazwa_pliku, nazwa_folderu, kanal=0):
    data = pd.read_csv("https://raw.githubusercontent.com/RusieckiFilip/PracaInz/main/"+
                       nazwa_folderu+"/H2-pow_fi1/"+nazwa_pliku, sep = ";")
    
    #### USUWANIE SZUMU ######
    if kanal != 0:
        i=0
        for j in data[kanal]:
            if data[kanal][i] > 0.45:
                data[kanal] = data[kanal].drop(labels=list(range(i,31999)), axis=0)    
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

data1 = wczytanie_danych("test1.csv","TESTY_H2-pow_fi1_091121","ch 3")
text1 = wczytanie_danych("test1_t.csv","TESTY_H2-pow_fi1_091121")


data2 = wczytanie_danych("test2.csv","TESTY_H2-pow_fi1_091121","ch 3")
text2 = wczytanie_danych("test2_t.csv","TESTY_H2-pow_fi1_091121")

data3 = wczytanie_danych("test3.csv","TESTY_H2-pow_fi1_091121","ch 3")
text3 = wczytanie_danych("test3_t.csv","TESTY_H2-pow_fi1_091121")

data4 = wczytanie_danych("test4.csv","TESTY_H2-pow_fi1_091121","ch 3")
text4 = wczytanie_danych("test4_t.csv","TESTY_H2-pow_fi1_091121")

data5 = wczytanie_danych("test5.csv","TESTY_H2-pow_fi1_091121","ch 3")
text5 = wczytanie_danych("test5_t.csv","TESTY_H2-pow_fi1_091121")

data6 = wczytanie_danych("test6.csv","TESTY_H2-pow_fi1_091121","ch 3")
text6 = wczytanie_danych("test6_t.csv","TESTY_H2-pow_fi1_091121")

data7 = wczytanie_danych("Exp_07.csv","testy_H2-pow_fi1_061221","ch 3")
text7 = wczytanie_danych("Exp_07_t.csv","testy_H2-pow_fi1_061221")

data8 = wczytanie_danych("Exp_08.csv","testy_H2-pow_fi1_061221","ch 3")
text8 = wczytanie_danych("Exp_08_t.csv","testy_H2-pow_fi1_061221")

############ FUNKCJA TWORZACA WYKRESY ######################################################

####### Funkcja(dane z czujnikow, opis, numer exp, trigger dla SN, trigger dla SN powrotna fala, trigger dla SJ, trig dla 2 pierwszych SN, czas po ktorym mierzymy trigger powrotnej fali) 

def funkcja(data1,text1,numer,tr_SN, tr_SN_f2, tr_SJ, tr_SN2, czas_zbior):
    
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
    #####################################################
    

    
    ########################## WYKRES ODCZYTÓW CZUJNIKÓW #################################
        
        
    fig1 = plt.figure("data" + numer)
    plt.clf()
    
    fig1.suptitle(opis, fontsize=14)
    
    ax1=plt.subplot(211)
    plt.style.use('seaborn-deep')
    plt.xlabel("Czas [us]")
    plt.ylabel("P [MPa]")
    plt.grid(color='#717171', linestyle='--', linewidth=0.3)
    #plt.ylim(0,2.5)
    plt.xlim(0,12000)
    #color = cm.rainbow(np.linspace(0, 1, 8))
    for i in range(1,9):
        plt.plot(data1["time [us]"],data1["ch "+ str(i)], linewidth=1, label =  "ch"+ str(i) + " SN")
    plt.legend(loc="lower right")
        
    ax1=plt.subplot(212)
    plt.style.use('seaborn-deep')
    plt.xlabel("Czas [us]")
    plt.ylabel("P [V]")
    plt.grid(color='#717171', linestyle='--', linewidth=0.3)
    #plt.ylim(0,2.5)
    plt.xlim(0,12000)
    for i in range(1,15):
        if i > 8:
            plt.plot(data1["time [us]"],data1["ch "+ str(i)], linewidth=1, label =  "ch"+ str(i) + " SJ" )
    plt.legend(loc="lower right")
    
    fig1.tight_layout()
    
    list3=temp
    list4=[0.1,4]
    l=-1
    
        ################ WYKRES ZBIORCZY ####################
    
    fig4 = plt.figure("Zbiorczy" + numer)
    plt.clf()
    
    fig4.suptitle(opis, fontsize=14)
    zbiorczy = plt.subplot(111)
    
    plt.style.use('seaborn-deep')
    plt.xlabel("Czas [us]")
    plt.ylabel("P[MPa] + x[m]")
    plt.grid(color='#717171', linestyle='--', linewidth=0.3)
    #plt.ylim(0,2.5)
    plt.xlim(0,13000)
    color = cm.rainbow(np.linspace(0, 1, 8))
    for i, c in zip(range(1,9),color):
        plt.plot(data1["time [us]"],data1["ch "+ str(i)] + df1["Odleglosc"][i-1], 
                 linewidth=0.4, label = "ch"+ str(i) + " SN, " + str(df1["Odleglosc"][i-1])+" m", c=c)
    plt.legend(loc="upper left")
    
    
    
    
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
    
    fig2 = plt.figure("TOA" + str(numer))
    plt.clf()
    
    fig2.suptitle('ToA\n\n' + opis, fontsize=14)
    
    plt.style.use('seaborn-deep')
    plt.xlabel("Dystans [m]")
    plt.ylabel("Czas [ms]")
    plt.grid(color='#717171', linestyle='--', linewidth=0.3)
    plt.xlim(0,3)
    
    
    plt.plot([0,df1["Odleglosc"][0]],[0,df1["TOA_P [ms]"][0]], linestyle='--', color="g")
    plt.plot([0,df1["Odleglosc"][2]],[0,df1["TOA_V [ms]"][2]], linestyle='--', color="b")
    
    
    plt.plot(df1["Odleglosc"],df1["TOA_P [ms]"], color="g", label="Fala cisnieniowa")
    plt.plot(df1["Odleglosc"][2:],df1["TOA_V [ms]"][2:], color="b", label="Front plomienia")
    plt.legend()
    fig2.tight_layout()
    
    
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
    print("Eksperyment: "+numer)
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
        if j < 7 and (p > 1750 or (list6[j-1]>0 and list6[j+1]>0 and p < 0) or p > 5*(list6[j-1]+list6[j+1])/2 ):
            if (list6[j-1]<0 and list6[j+1]<0 and p < 0): list6[j] = ((list6[j-1])+(list6[j+1]))/2
            else: list6[j] = (abs(list6[j-1])+abs(list6[j+1]))/2 
        elif j < 7 and (v > 1750 or (list7[j-1]>0 and list7[j+1]>0 and v < 0) or v > 5*(list7[j-1]+list7[j+1])/2):
            if (list7[j-1]<0 and list7[j+1]<0 and v < 0): list7[j] = ((list7[j-1])+(list7[j+1]))/2 
            else: list7[j] = list7[j] = (abs(list7[j-1])+abs(list7[j+1]))/2
       
    #################
    
        else: ########### USUWAM UJEMNE WARTOSCI ALE CZY POPRAWNIE  ???????   ###########
            list6[j]=abs(list6[j])
            list7[j]=abs(list7[j])
            
    ################
    
    fig3 = plt.figure("V" + numer)
    plt.clf()
    
    fig3.suptitle('dx/dt\n\n' + opis, fontsize=14)
    
    plt.style.use('seaborn-deep')
    plt.xlabel("Dystans [m]")
    plt.ylabel("Predkosc [m/s]")
    plt.grid(color='#717171', linestyle='--', linewidth=0.3)
    
    plt.plot([0,list5[1]],[0,list6[1]], linestyle='--', color="g")
    plt.plot([0,list5[2]],[0,list7[2]], linestyle='--', color="b")
    
    plt.plot(list5[1:],list6[1:], label="Fala cisnieniowa", color="g")
    plt.plot(list5[2:],list7[2:], label="Front plomienia",  color="b")
    
    
    plt.plot([0,3.5], [1979.24,1979.24], linestyle='-.', color = "r", linewidth=1.3, alpha=0.6)
    plt.xlim(0,3)
    plt.text(0.1, 2000, r'$V_{CJ}=1979.24\ [m/s]$', fontsize=10)
    
    
    plt.legend()
    fig3.tight_layout()
    
    
    
    
    

    
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
                    else: list_zbior.append(data[i][k-2500]+o-0.3)
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
    
    zbiorczy.plot(list_czas, list_zbior,
                  linewidth=2, color='k')

    
    return df1
    
    




##########################################################################################################

###### WYSWIETLENIE WYKRESOW #############################################################################

####### Funkcja(dane z czujnikow, opis, numer exp, trigger dla SN, trigger dla SN powrotna fala,
####### trigger dla SJ, trig dla 2 pierwszych SN, czas po ktorym mierzymy trigger powrotnej fali) 

df1=funkcja(data1,text1,"1",0.25,0.9,0.08,0.15,6200)
df2=funkcja(data2,text2,"2",0.25,1.1,0.225,0.25,6200)
#funkcja(data3,text3,"3",0.15,0.6) ##### jedna sonda nie dziala (sonda 4)
df4=funkcja(data4,text4,"4",0.25,0.31,0.11,0.15,7500)
df5=funkcja(data5,text5,"5",0.25,0.28,0.12,0.15,7500)
df6=funkcja(data6,text6,"6",0.25,0.35,0.049,0.231,7500) 
df7=funkcja(data7,text7,"7",0.35,0.65,0.05,0.231,6700) 
df8=funkcja(data8,text8,"8",0.17,0.4,0.2,0.2,6500) 






























# ##### Zbiorcze wykresy predkosci i ToA

# def wykres_zbiorczy(sred_odleg,V_p,V_v,numer):
  
#     plt.plot([0,sred_odleg[1]],[0,V_p[1]], linestyle='--')
#     plt.plot([0,sred_odleg[2]],[0,V_v[2]], linestyle='--')
    
#     plt.plot(sred_odleg[1:],V_p[1:], label="Fala cisnieniowa exp."+str(numer))
#     plt.plot(sred_odleg[2:],V_v[2:], label="Front plomienia exp."+str(numer))

   
# fig3 = plt.figure("V")

# fig3.suptitle('dx/dt' , fontsize=14)
    
# plt.style.use('seaborn-deep')
# plt.xlabel("Dystans [m]")
# plt.ylabel("Predkosc [m/s]")
# plt.grid(color='#717171', linestyle='--', linewidth=0.3)
  
# wykres_zbiorczy(df1["Srednia odleglosc"],df1["Predkosc P"],df1["Predkosc V"],1)
# wykres_zbiorczy(df2["Srednia odleglosc"],df1["Predkosc P"],df1["Predkosc V"],2)
# #wykres_zbiorczy(df3["Srednia odleglosc"],df1["Predkosc P"],df1["Predkosc V"])
# wykres_zbiorczy(df4["Srednia odleglosc"],df1["Predkosc P"],df1["Predkosc V"],4)
# wykres_zbiorczy(df5["Srednia odleglosc"],df1["Predkosc P"],df1["Predkosc V"],5)
# wykres_zbiorczy(df6["Srednia odleglosc"],df1["Predkosc P"],df1["Predkosc V"],6)
        
# plt.plot([0,3.5], [1979.24,1979.24], linestyle='-.', color = "r", linewidth=1.3, alpha=0.6)
# plt.xlim(0,3)
# plt.text(0.1, 2000, r'$V_{CJ}=1979.24\ [m/s]$', fontsize=10)
    
    
# plt.legend()
# fig3.tight_layout()

