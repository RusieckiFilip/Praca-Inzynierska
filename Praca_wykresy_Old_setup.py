

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

# data3 = wczytanie_danych("test3.csv","TESTY_H2-pow_fi1_091121","ch 3")
# text3 = wczytanie_danych("test3_t.csv","TESTY_H2-pow_fi1_091121")

# data4 = wczytanie_danych("test4.csv","TESTY_H2-pow_fi1_091121","ch 3")
# text4 = wczytanie_danych("test4_t.csv","TESTY_H2-pow_fi1_091121")

# data5 = wczytanie_danych("test5.csv","TESTY_H2-pow_fi1_091121","ch 3")
# text5 = wczytanie_danych("test5_t.csv","TESTY_H2-pow_fi1_091121")

# data6 = wczytanie_danych("test6.csv","TESTY_H2-pow_fi1_091121","ch 3")
# text6 = wczytanie_danych("test6_t.csv","TESTY_H2-pow_fi1_091121")

data7 = wczytanie_danych("Exp_07.csv","testy_H2-pow_fi1_061221","ch 3")
text7 = wczytanie_danych("Exp_07_t.csv","testy_H2-pow_fi1_061221")

data8 = wczytanie_danych("Exp_08.csv","testy_H2-pow_fi1_061221","ch 3")
text8 = wczytanie_danych("Exp_08_t.csv","testy_H2-pow_fi1_061221")

# data9 = wczytanie_danych("Exp_05.csv","testy_H2-pow_fi08_061221","ch 3")
# text9 = wczytanie_danych("Exp_05_t.csv","testy_H2-pow_fi08_061221")

# data10 = wczytanie_danych("Exp_06.csv","testy_H2-pow_fi08_061221","ch 3")
# text10 = wczytanie_danych("Exp_06_t.csv","testy_H2-pow_fi08_061221")

# data11 = wczytanie_danych("Exp_07.csv","testy_H2-pow_fi08_071221","ch 3")
# text11 = wczytanie_danych("Exp_07_t.csv","testy_H2-pow_fi08_071221")

# data12 = wczytanie_danych("Exp_08.csv","testy_H2-pow_fi08_071221","ch 3")
# text12 = wczytanie_danych("Exp_08_t.csv","testy_H2-pow_fi08_071221")

data13 = wczytanie_danych("Exp_09.csv","testy_H2-pow_fi1_13122021","ch 3")
text13 = wczytanie_danych("Exp_09_t.csv","testy_H2-pow_fi1_13122021")

# data14 = wczytanie_danych("Exp_010.csv","testy_H2-pow_fi1_13122021","ch 3")
# text14 = wczytanie_danych("Exp_010_t.csv","testy_H2-pow_fi1_13122021")

# data15 = wczytanie_danych("Exp_011.csv","testy_H2-pow_fi1_13122021","ch 3")
# text15 = wczytanie_danych("Exp_011_t.csv","testy_H2-pow_fi1_13122021")

# data16 = wczytanie_danych("Exp_01.csv","testy_H2-pow_fi16_13122021","ch 3")
# text16 = wczytanie_danych("Exp_01_t.csv","testy_H2-pow_fi16_13122021")

# data17 = wczytanie_danych("Exp_02.csv","testy_H2-pow_fi16_13122021","ch 3")
# text17 = wczytanie_danych("Exp_02_t.csv","testy_H2-pow_fi16_13122021")

# data18 = wczytanie_danych("Exp_03.csv","testy_H2-pow_fi16_13122021","ch 3")
# text18 = wczytanie_danych("Exp_03_t.csv","testy_H2-pow_fi16_13122021")

# data19 = wczytanie_danych("Exp_04.csv","testy_H2-pow_fi16_13122021","ch 3")
# text19 = wczytanie_danych("Exp_04_t.csv","testy_H2-pow_fi16_13122021")



############ FUNKCJA TWORZACA WYKRESY ######################################################

####### Funkcja(dane z czujnikow, opis, numer exp, trigger dla SN, trigger dla SN powrotna fala, trigger dla SJ, trig dla 2 pierwszych SN, czas po ktorym mierzymy trigger powrotnej fali, max dopusz predkosc fizyczna) 

def funkcja(data1,text1,numer,tr_SN, tr_SN_f2, tr_SJ, tr_SN2, czas_zbior, V_max):
    
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
        
        
    fig1 = plt.figure("data" + numer,figsize=(16, 9), dpi=150)
    plt.clf()
    
    fig1.suptitle(opis, fontsize=20)
    
    ax1=plt.subplot(211)
    plt.style.use('seaborn-deep')
    plt.xlabel("Czas [us]", fontsize=15)
    plt.ylabel("P [MPa]", fontsize=15)
    plt.grid(color='#717171', linestyle='--', linewidth=0.3)
    #plt.ylim(0,2.5)
    plt.xlim(2000,12000)
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
    #plt.ylim(0,2.5)
    plt.xlim(2000,12000)
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
    
    fig4.suptitle(opis, fontsize=23)
    zbiorczy = plt.subplot(111)
    
    plt.style.use('seaborn-deep')
    plt.xlabel("Czas [us]", fontsize=17)
    plt.ylabel("P[MPa] + x[m]", fontsize=17)
    plt.grid(color='#717171', linestyle='--', linewidth=0.3)
    #plt.ylim(0,2.5)
    plt.xlim(2000,14000)
    color = cm.rainbow(np.linspace(0, 1, 8))
    for i, c in zip(range(1,9),color):
        plt.plot(data1["time [us]"],data1["ch "+ str(i)] + df1["Odleglosc"][i-1], 
                 linewidth=1, label = "ch"+ str(i) + " SN, " + str(df1["Odleglosc"][i-1])+" m", c=c)
    plt.tick_params(axis='both', labelsize=16)
    plt.legend(loc="upper left", fontsize=15)
    
    
    
    
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
    
    fig2.suptitle('ToA\n\n' + opis, fontsize=23)
    
    plt.style.use('seaborn-deep')
    plt.xlabel("Dystans [m]", fontsize=17)
    plt.ylabel("Czas [ms]", fontsize=17)
    plt.grid(color='#717171', linestyle='--', linewidth=0.3)
    plt.xlim(0,3)
    plt.tick_params(axis='both', labelsize=16)
    
    
    plt.plot([0,df1["Odleglosc"][0]],[0,df1["TOA_P [ms]"][0]], linestyle='--', color="g")
    plt.plot([0,df1["Odleglosc"][2]],[0,df1["TOA_V [ms]"][2]], linestyle='--', color="b")
    
    
    plt.plot(df1["Odleglosc"],df1["TOA_P [ms]"], color="g", label="Fala cisnieniowa",marker="o")
    plt.plot(df1["Odleglosc"][2:],df1["TOA_V [ms]"][2:], color="b", label="Front plomienia",marker="o")
    plt.legend(fontsize=15, loc="upper left")
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
    
    fig3 = plt.figure("V" + numer)
    plt.clf()
    
    fig3.suptitle('dx/dt\n\n' + opis, fontsize=23)
    
    plt.style.use('seaborn-deep')
    plt.xlabel("Dystans [m]", fontsize=17)
    plt.ylabel("Predkosc [m/s]", fontsize=17)
    plt.grid(color='#717171', linestyle='--', linewidth=0.3)
    
    plt.plot([0,list5[1]],[0,list6[1]], linestyle='--', color="g")
    plt.plot([0,list5[2]],[0,list7[2]], linestyle='--', color="b")
    
    plt.plot(list5[1:],list6[1:], label="Fala cisnieniowa", color="g",marker="o")
    plt.plot(list5[2:],list7[2:], label="Front plomienia",  color="b",marker="o")
    plt.ylim(0,2100)
    plt.tick_params(axis='both', labelsize=16)
    
    plt.plot([0,3.5], [1979.24,1979.24], linestyle='-.', color = "r", linewidth=1.5, alpha=0.6)
    plt.plot([0,3.5], [1108.5,1108.5], linestyle='-.', color = "r", linewidth=1.5, alpha=0.6)
    plt.xlim(0,3)
    plt.text(0.1, 2000, r'$V_{CJ}=1979.24\ [m/s]$', fontsize=15)
    plt.text(0.1, 1140, r'$a_{p}=1108.5\ [m/s]$', fontsize=15)
    
    
    plt.legend(fontsize=17, loc="upper right")
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

####### TESTY_H2-pow_fi1_091121 #############
  
df1=funkcja(data1,text1,"1",0.25,0.9,0.08,0.15,6200,1750)
df2=funkcja(data2,text2,"2",0.25,1.1,0.225,0.25,6200,1750)
####funkcja(data3,text3,"3",0.15,0.6) ##### jedna sonda nie dziala (sonda 4)
# df4=funkcja(data4,text4,"4",0.25,0.31,0.11,0.15,7500,1750)
# df5=funkcja(data5,text5,"5",0.25,0.28,0.12,0.15,7500,1750)
# df6=funkcja(data6,text6,"6",0.25,0.35,0.049,0.231,7500,1750) 

# ######## testy_H2-pow_fi1_061221 ###########

df7=funkcja(data7,text7,"7",0.35,0.8,0.05,0.231,6700,1750) 
df8=funkcja(data8,text8,"8",0.17,0.8,0.2,0.2,6500,1750) 

######## testy_H2-pow_fi08_061221 ###########

# df9=funkcja(data9,text9,"9",0.22,0.25,0.05,0.14,9000,1300) #Sprawdzic dane sond
# df10=funkcja(data10,text10,"10",0.17,0.35,0.044,0.2,9800,1100) 

########  testy_H2-pow_fi08_071221 #########

# df11=funkcja(data11,text11,"11",0.203,0.95,0.3,1.2,7250,2000)
# df12=funkcja(data12,text12,"12",0.29,0.35,0.044,0.2,10130,1111) 

######## testy_H2-pow_fi1_13122021  #########

df13=funkcja(data13,text13,"13",0.203,0.65,0.07,0.2,6750,2000)
# df14=funkcja(data14,text14,"14",0.29,0.4,0.1,0.2,7500,2000) 
# df15=funkcja(data15,text15,"15",0.29,0.4,0.08,0.2,7500,2000) 

#######  testy_H2-pow_fi16_13122021 #############

# df16=funkcja(data16,text16,"16",0.3,1,0.07,0.3,3770,1700)
# df17=funkcja(data17,text17,"17",0.25,0.25,0.15,0.1135,6600,2000) 
# df18=funkcja(data18,text18,"18",0.137,0.4,0.08,0.3,6500,2000) 
# df19=funkcja(data19,text19,"19",0.2,0.4,0.07,0.3,6660,2000)



####### ZBIORCZY ###########

dane_f1 =  pd.read_csv("https://raw.githubusercontent.com/RusieckiFilip/PracaInz/main/zbiorczy_fi1.csv", sep = ";")


w = 0.5    # bar width
x = [1] # x-coordinates of your bars
colors = [(0, 0, 1, 1)]    # corresponding colors
y = [dane_f1["ITD."]]



fig, ax = plt.subplots()


    
fig.suptitle('Opoznienie zaplonu od stezenia', fontsize=23)
    
plt.style.use('seaborn-deep')
plt.xlabel("Stezenie mieszaniny", fontsize=17)
plt.ylabel("Opoznienie zaplonu [us]", fontsize=17)
plt.grid(color='#717171', linestyle='--', linewidth=0.3)
plt.yscale("log")
    
plt.tick_params(axis='both', labelsize=16)

ax.bar(x,
       height=[np.mean(yi) for yi in y],
       yerr=[np.std(yi) for yi in y],    # error bars
       capsize=0, # error bar cap width in points
       width=0,    # bar width
       tick_label=["fi=1"],
       color=(0,0,0,0),  # face color transparent
       edgecolor=(0,0,0,0),
       #ecolor=colors,    # error bar colors; setting this raises an error for whatever reason.
       )
#### tworzenie markow #####
mark=[]
for i in range(len(dane_f1["ITD."])):
    if dane_f1["kat"][i]==0: mark.append("X")
    elif dane_f1["kat"][i]==1: mark.append((5, 1))
    elif dane_f1["kat"][i]==2: mark.append("o")
    elif dane_f1["kat"][i]==3: mark.append("s")
    
# fi = 1
for i, m, y_ in zip(range(len(mark)), mark, dane_f1["ITD."]) :
    # distribute scatter randomly across whole width of bar
    ax.scatter(x[0] + np.random.random(y[0].size)[i] * w - w / 2, y_, color=colors[0], marker=m)


custom_marks = [Line2D([0], [0], marker='X', color='w', label='Brak zaplonu',
                          markerfacecolor='k', markersize=15),
                Line2D([0], [0], marker='s', color='w', label='Przedwczesna detonacja',
                          markerfacecolor='k', markersize=15),
                Line2D([0], [0], marker='o', color='w', label='Opozniony zaplon',
                          markerfacecolor='k', markersize=15),
                Line2D([0], [0], marker=(5, 1), color='w', label='Detonacja na narozu',
                          markerfacecolor='k', markersize=15)]

plt.legend(handles = custom_marks,fontsize=17, loc="best")





#   ########################## WYKRES ITD i CISNIENIA OD PREDKOSCI #################################

# def monoExp(x, m, t, b):
#     return m * np.exp(-t * x) + b

# xs=dane_f1["predkosc"]
# ys=dane_f1["ITD."]

# # perform the fit
# p0 = (610, 0.1, -6000) # start with values near those we expect
# params, cv = scipy.optimize.curve_fit(monoExp, xs, ys, p0)
# m, t, b = params
# sampleRate = 20_000 # Hz
# tauSec = (1 / t) / sampleRate

# # determine quality of the fit
# squaredDiffs = np.square(ys - monoExp(xs, m, t, b))
# squaredDiffsFromMean = np.square(ys - np.mean(ys))
# rSquared = 1 - np.sum(squaredDiffs) / np.sum(squaredDiffsFromMean)
# print(f"R² = {rSquared}")

# # plot the results
# plt.clf()
# plt.plot(xs, ys, '.', label="data")
# plt.plot(xs, monoExp(xs, m, t, b), '--', label="fitted")
# plt.title("Fitted Exponential Curve")

# # inspect the parameters
# print(f"Y = {m} * e^(-{t} * x) + {b}")
# print(f"Tau = {tauSec * 1e6} µs")
        
# fig1 = plt.figure("ITD(V)",figsize=(16, 9), dpi=150)
# plt.clf()
    
# fig1.suptitle("ITD(V)", fontsize=17)
    

# plt.style.use('seaborn-deep')
# plt.xlabel("Predkosc [m/s]", fontsize=13)
# plt.ylabel("ITD [us]", fontsize=13)
# plt.grid(color='#717171', linestyle='--', linewidth=0.3)
# #plt.ylim(0,2.5)
# #plt.xlim(2000,12000)
# plt.scatter(dane_f1["predkosc"],dane_f1["ITD."])
# plt.yscale("log")


# #plt.legend(loc="upper left", fontsize=11)
# plt.tick_params(axis='both', labelsize=12)
    
# fig1.tight_layout()






