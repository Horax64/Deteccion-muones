import sys
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy import signal
import numpy as np
import pandas as pd

num = int(sys.argv[1])
print(f"medicion num: {num}")

data = pd.read_csv('mediciones/data.txt', sep=r"\s+", header=None, names=["t1[ns]","u1[mV]","u2[mV]","u3[mV]"])

trig = -60 #mV

if data["u1[mV]"].min() <= trig:
	u1 = data["u1[mV]"]
	u2 = data["u2[mV]"]
	u3 = data["u3[mV]"]
	t = data ["t1[ns]"]
	p1,_ = find_peaks(-u1,distance=200,threshold=-trig)
	p3,_ = find_peaks(-u3,distance=200,threshold=-trig)
	
	if len(p1) >= 1 and len(p3) >=1:
		print(p1)
		print(p3)
		print("------------------------------------------> Señal 1 y 3")
		if np.abs(p1[0] - p3[0]) <= 200:
			data.to_csv(f"mediciones/prueba_eficiencia_cent2_2/data_{num:04d}.txt")
			print("------------------------------------------> Medición útil")
		else: print("------------------------------------------> Falsa señal")
	else: print("------------------------------------------> No hay señal en 3")
