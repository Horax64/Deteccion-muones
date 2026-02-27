import sys
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy import signal
import numpy as np


num = int(sys.argv[1])  # Convertir el argumento a entero
print(f"medicion numero {num}")

# Lee el archivo data.txt y carga los datos en un DataFrame
data = pd.read_csv('mediciones/data.txt', sep=r"\s+", header=None, names=["t1[ns]", "u1[mV]", "u2[mV]", "u3[mV]"])

trig = -60 # [mV]

def peak(eje_x,eje_y,n,umbral):

    picos= signal.find_peaks(eje_y,distance = n)[0] #encuentra los indices de los picos

    #creo dos variables para almacenar los datos en los picos
    y_picos=[]
    x_picos=[]
    p = np.array([])

    for i in picos:
        if eje_y[i] > umbral:
            y_picos.append(eje_y[i])
            x_picos.append(eje_x[i])


    return (np.array(x_picos),np.array(y_picos))

if data["u1[mV]"].min() <= trig:
    u1 = data["u1[mV]"]
    u2 = data["u2[mV]"]
    u3 = data["u3[mV]"]
    t = data["t1[ns]"]
    p1 = peak(t,-u1,200,60)
    p2 = peak(t,-u2,200,60)
    p3 = peak(t,-u3,200,60)
    print("----------------------------------------------------------------------> pulsos en UP")    
    
	if len(p1[0]) >= 1 and len(p3[0]) >= 1:
		if (p1[0][0] - p3[0][0]) < 200*t[1]:
			data.to_csv(f"mediciones/prueba_eficiencia_cent2_2/data_{num:04d}.txt")
			print("-------------------------------------------------------------------- ---------------> Señal 1 y 3 valida")
		else: print("-------------------------------------------------------------------- ---------------> Señal 1 y 3 falsa")
	else: print("-----------------------------------------------------------------------> no hay coincidencias")
