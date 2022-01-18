#!/usr/bin/python3
from random import randint


array = []
for i in range(4):
    array.append( randint(0, 10) )

print(array)

new_array = []

while True:
    bigger = 0
    index = 0
    for i in range( len(array) ):
        if array[i] >= bigger:
            bigger = array[i]
            index = i
    new_array.append(array[index])
    array.pop(index)

    if len(array) == 0:
        break
print(new_array)