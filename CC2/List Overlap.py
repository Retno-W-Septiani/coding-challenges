## items present in both lists
list_a = ['dog', 'cat', 'rabbit', 'hamster', 'gerbil']
list_b = ['dog', 'hamster', 'snake']
# list_c = [value for value in list_a if value in list_b]
# print(list_c)

# or
# list_c = list(set(list_a) & set(list_b))
# print(list_c)

#or
# for i in list_a and list_b:
#     print(i)

## non-overlapping items in the lists
# list_d = list(set(list_a) ^ set(list_b))
# print(list_d)