from scipy.special import spherical_jn as jn #Сферическая функция Бесселя первого порядка
from scipy.special import spherical_yn as yn #Сферическая функция Бесселя второго порядка
import matplotlib.pyplot as plt
import urllib.request as url # открытие url
from numpy import pi #упрощение записи pi
from re import split #расщепление массива
import numpy as np
import os
# вычисление начальных данных для расчёта ЭПР
def hn(l, z):
 return jn(l, z) + 1j * yn(l, z)
def an(l, z):
 return jn(l, z) / hn(l, z)
def bn(l, z):
 return (z * jn(l - 1, z) - l * jn(l, z)) \
 / (z * hn(l - 1, z) - l * hn(l, z))
# вывод исходных данных
URL = 'https://jenyay.net/uploads/Student/Modelling/task_02.txt'
file = url.urlopen(URL)
list = file.readlines()
my_string = list[15].decode("utf-8") # принимает первую строку за 0
values = split("[=\r;]", my_string) # парсинг значений
D = float(values[1])
fmin = float(values[3])
fmax = float(values[5])
Z = 10000 # число точек на отрезке
r = 0.5 * D
f = np.linspace(fmin, fmax, Z) # указываем количество элементов
L = 3e8 / f
k = 2 * pi / L
Sum_arr = [((-1) ** n) * (n + 0.5) * (an(n, k * r) - bn(n, k * r)) \
 for n in range(1, 50)]
Sum = np.sum(Sum_arr, axis=0) # суммирование элементов массива
Sig = (L ** 2) / pi * (np.abs(Sum) ** 2) # вычисление ЭПР
plt.plot(f/0.01e9, Sig) # построение графика
plt.xlabel('$f, МГц$')
plt.ylabel('$\sigma, м^2$')
plt.grid() # создание сетки
plt.show()
# указываем путь
try:
 os.mkdir('results')
except OSError:
 pass
2
complete_file = os.path.join('results', 'task_02_307B_Pogudin_16.txt')
# преобразуем nparray в list, для облегчения работы с многомерным массивом
ftl = f.tolist() 
Stl = Sig.tolist()
f = open(complete_file, 'w')
f.write('    f         Sigma\n')
#расчёт значений для заданного количества точек
for i in range(Z):
 #ftl[i] = ftl[i]/1e7
 #Stl[i] = Stl[i]/1e6
 f.write(str("%.2f" % ftl[i])+' '+str("%.8f" % Stl[i])+"\n")
f.close()

