#задача: удалить N строк из заданного файла

import random
import math

def input_number(max_val, s):
    D = 0
    while D <= 0 or D > max_val:
        D = int(input(s))
    return D

sortList= [] #сорта атомов
list = []    #общий список значений
Ed = []      #дельта энергии, все значения E не отрицательны
Eps = []     #накопительная сумма от вероятности для элемента (изначальной строки) быть удаленной
Emin = 0.0   #наименьшее значение E
zeros_count = 4
Energy_col = 4

path_name = str(input('Введите название исходного файла: '))
if '.XYZ' not in path_name:
    path_name += '.XYZ'

work_file = open(path_name) #открываем файл с исходными данными
N = int(work_file.readline())
D = input_number(3 * N // 10, 'Введите число строк для удаления: ')

sum_dist = 0
j = 2        #номер по порядку
for i in work_file:
    if j > 2:
        work_list = []  # отдельно взятая строка
        k = i.split()  # считываем строку, удаляем пробелы

        for g in range(len(k)):
            if g == 0: # сорт это строка
                sortList.append(k[0])
            else: # всё остальное - числа
                xyzE = float(k[g])
                work_list.append(xyzE)
                if (g == Energy_col) and (xyzE < Emin):
                    Emin = xyzE

        dist = sum(xyz**2 for xyz in work_list[0:3]) ** (1/2)
        sum_dist += dist

        work_list.append(j-2) # номер в исходном
        work_list.append(dist) # расстояние до центра
        list.append(work_list)

    j += 1

work_file.close()   #закрытие рабочего файла с исходными значениями

avg_dist = sum_dist / N
print('avg_dist = ', avg_dist)
core_list = [int(item[4]) for item in list if item[5] < avg_dist]

for wlist in list:
    eNorm = wlist[Energy_col - 1] - Emin
    eNorm = eNorm ** (3/2)
    Ed.append(eNorm)

sum_Ed = sum(Ed)
print('sum_Ed = ', sum_Ed)
#print(sum(float(wlist[4]) for wlist in list))

cum = 0.0
for i in Ed:
    cum += i / sum_Ed
    Eps.append(cum)

del_list = []    #номер строки на удаление
d = D
while d > 0:
    p = random.uniform(0, 1)    #генерируем случайное число p от 0 до 1
    k = 0
    for j in range(len(Eps)):
        if Eps[j] >= p:
            k = j
            break

    if (k in del_list) or (k in core_list):
        continue
    else:
        del_list.append(k)
        d -= 1

#справочная информация
print('core_list', core_list)
print('del_list', del_list)
print('list', list)
print('Ed', Ed)
print('Eps', Eps)
print('Done. Emin=', Emin)

#запись значений в итоговый файл
final_file = open(path_name[0:len(path_name)-4] + "_delete_" + str(D).zfill(zeros_count) + ".XYZ", "w")    #открываем файл для записи
final_file.write(str(N - D))
final_file.write('\n')

freq = dict()
for k in range(len(sortList)):
    if k not in del_list:
        item = sortList[k]
        freq[item] = freq.get(item, 0) + 1

counts = ""
for element in sorted(freq.keys(), reverse = True):
    counts += element + '_' + str(freq[element]).zfill(zeros_count) + '_'

final_file.write(counts)
final_file.write('\n')

for i in range(len(list)):
    if i not in del_list:
        final_file.write(sortList[i] + '\t')
        final_file.write('\t'.join('{:.4f}'.format(j) for j in list[i]))
        final_file.write('\n')

final_file.close()  #закрытие итогового файла 
