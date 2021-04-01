# import itertools
# print(len(list(itertools.permutations('ABCD', 4))))
# #print(list(itertools.permutations([1, 2, 3])))
#
#
# for i in "hola":
#     for j in range(0, 4):
#         if i == "l":
#             break
#         print(i,j)

numero_columnas = 3
numero_filas = 4
matriz = [[0] * numero_columnas for i in range(numero_filas)]
matriz[2][1] = "t"
matriz[3][2] = 2
for i in matriz:
    print(i)

