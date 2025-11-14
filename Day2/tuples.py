
# Tuples, unmutatable structure
tuple_1 = (1, 2, 3, 4)
tuple_2 = 1., .5, .25, .125
tuple_3 = tuple_1 * 3
tuple_4 = tuple_1 + (1000, 2000)


tuple_1[0]
tuple_1[-1]
tuple_1[1:]
tuple_1[:-2]

for element in tuple_1:
    print(element)
