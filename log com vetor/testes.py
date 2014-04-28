import math

primeiro, segundo = 0.5, 1.5
modificador = divmod(primeiro, 0.5)
m = modificador[0]
index = divmod(segundo, 0.5)
i = index[0]
# if(i > 0):
#     i = i -1
indice = i + (m * (10/0.5))
print modificador, index, int(indice)

print(divmod(20, 0.5))