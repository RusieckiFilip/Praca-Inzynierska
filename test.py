

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import re 

############ WCZYTANIE DANYCH O CZUJNIKACH ######################################################

xxx = pd.read_csv("C:\\Users\\Filip\\Desktop\\PRACA INZ\\Python\\VMPA.csv", sep = ";")

for i in xxx["SN"]:
    if type(i)==int:
        i = str(i)
        
####### FUNKCJA WCZYTANIA DANYCH ###############################################################################

def wczytanie_danych(nazwa_pliku, kanal=0):
    data = pd.read_csv("C:\\Users\\Filip\\Desktop\\PRACA INZ\\Python\\Dane_10.11.2021\\TESTY_H2-pow_fi1_091121\\H2-pow_fi1\\"+nazwa_pliku, sep = ";")
    if kanal != 0:
        i=0
        for j in data[kanal]:
            if data[kanal][i] > 0.35:
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

################### DROP DANYCH PRZED 3000 sekunda i dla kanału 3 ################################

############# WCZYTANIE DANYCH ##########################################################################################################################

data1 = wczytanie_danych("test1.csv","ch 3")
text1 = wczytanie_danych("test1_t.csv")


data2 = wczytanie_danych("test2.csv","ch 3")
text2 = wczytanie_danych("test2_t.csv")

data3 = wczytanie_danych("test3.csv","ch 3")
text3 = wczytanie_danych("test3_t.csv")

data4 = wczytanie_danych("test4.csv","ch 3")
text4 = wczytanie_danych("test4_t.csv")

data5 = wczytanie_danych("test5.csv","ch 3")
text5 = wczytanie_danych("test5_t.csv")

data6 = wczytanie_danych("test6.csv","ch 3")
text6 = wczytanie_danych("test6_t.csv")


############ FUNKCJA TWORZACA WYKRESY ######################################################

####### Funkcja(dane z czujnikow, opis, numer exp, trigger dla SN, trigger dla SJ) 

def funkcja(data1,text1,numer,tr_SN,tr_SJ):

    ######## Obliczanie TOA_P dla kanałow bez sond jonizacyjnych ##########################
    
    
    temp = []
    l = -1
    for i in data1:
        if i != "time [us]" and l < 2:
            k = -1
            for j in data1[i]:
                k += 1
                if data1[i][k] > tr_SN:
                    temp.append(data1["time [us]"][k]/1000)
                    break
        l += 1
    
    ######################################################################################
    
    
    
    #0%CH4+100%H2
    
    list1=[]
    for i in text1["Tabela"]:
        l=0
        for j in xxx["SN"]:
            if j in i:
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
        if  i != "time [us]" and l <8:
            data1[i] = data1[i]/df1["VPMA"][l]+0.1
        l+=1
    #####################################################
    
    ###### USUWANIE kanałow bez sond jonizacyjnych #################################
    
    data1.drop('ch 1',
      axis='columns', inplace=True)
    data1.drop('ch 2',
      axis='columns', inplace=True)
    
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
    #plt.xlim(14000,23000)
    for i in range(3,9):
        plt.plot(data1["time [us]"],data1["ch "+ str(i)], linewidth=1, label =  "ch"+ str(i) + " SN")
    plt.legend(loc="lower right")
        
    ax1=plt.subplot(212)
    plt.style.use('seaborn-deep')
    plt.xlabel("Czas [us]")
    plt.ylabel("P [V]")
    plt.grid(color='#717171', linestyle='--', linewidth=0.3)
    #plt.ylim(0,2.5)
    #plt.xlim(14000,23000)
    for i in range(1,15):
        if i > 8:
            plt.plot(data1["time [us]"],data1["ch "+ str(i)], linewidth=1, label =  "ch"+ str(i) + " SJ" )
    plt.legend(loc="lower right")
    
    fig1.tight_layout()
    
    list3=temp
    list4=[0.1,0.2]
    l=-1
    
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
    
    list5=[]
    l=1
    for i in df1["Odleglosc"]:
        if l<8:
            list5.append((df1["Odleglosc"][l]+df1["Odleglosc"][l-1])/2)
        l+=1
    #df1["Srednia odleglosc"]=list5
    
    
    ################### PREDKOSC FALI CISNIENIOWEJ ###########################
    
    list6=[]
    l=1
    print("Eksperyment: "+numer)
    for i in df1["TOA_P [ms]"]:
        if l<8:
            if (df1["Odleglosc"][l]-df1["Odleglosc"][l-1])/(df1["TOA_P [ms]"][l]-df1["TOA_P [ms]"][l-1])>100:
                list6.append(0)
            else: 
                list6.append((df1["Odleglosc"][l]-df1["Odleglosc"][l-1])*1000/(df1["TOA_P [ms]"][l]-df1["TOA_P [ms]"][l-1]))
                print("Odleglosc "+str(l+1)+" i", str(l),":", df1["Odleglosc"][l],",", df1["Odleglosc"][l-1], ";TOAP1-2:",
                      df1["TOA_P [ms]"][l],",",df1["TOA_P [ms]"][l-1])
            l+=1
    #df1["Predkosc P"]=list6
    
    ############# PREDKOSC PLOMIENIA #############################
    list7=[]
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
    #df1["Predkosc V"]=list7
    
       
    fig3 = plt.figure("V" + numer)
    plt.clf()
    
    fig3.suptitle('dx/dt\n\n' + opis, fontsize=14)
    
    plt.style.use('seaborn-deep')
    plt.xlabel("Dystans [m]")
    plt.ylabel("Predkosc [m/s]")
    plt.grid(color='#717171', linestyle='--', linewidth=0.3)
    
    plt.plot([0,list5[0]],[0,list6[0]], linestyle='--', color="g")
    plt.plot([0,list5[2]],[0,list7[2]], linestyle='--', color="b")
    
    plt.plot(list5,list6, label="Fala cisnieniowa", color="g")
    plt.plot(list5[2:],list7[2:], label="Front plomienia",  color="b")
    
    
    plt.plot([0,3.5], [1979.24,1979.24], linestyle='-.', color = "r", linewidth=1.3, alpha=0.6)
    plt.xlim(0,3)
    plt.text(0.1, 2000, r'$V_{CJ}=1979.24\ [m/s]$', fontsize=10)
    
    
    plt.legend()
    fig3.tight_layout()
    
    return opis



##########################################################################################################

###### WYSWIETLENIE WYKRESOW #############################################################################

funkcja(data1,text1,"1",0.25,0.5)
funkcja(data2,text2,"2",0.25,0.5)
#funkcja(data3,text3,"3",0.15,0.6) ##### jedna sonda nie dziala (sonda 4)
funkcja(data4,text4,"4",0.25,0.12)
funkcja(data5,text5,"5",0.25,0.12)
funkcja(data6,text6,"6",0.25,0.12)

