import sys
print("This is income calculator")
hourlywage_1 = int(sys.argv[1])
hourlywage_2 = int(sys.argv[2])
hourlywage_3 = int(sys.argv[3])

hourlywage_list = [hourlywage_1, hourlywage_2, hourlywage_3]

# condition
for hourlywage in hourlywage_list:
    print("... If hourly wage was - $" + str(hourlywage))
    print("Full time: ", "\n Daily:$", str(hourlywage*8), "\n Weekly:$", str(hourlywage*40), "\n Yearly:$", str(hourlywage*2080))
    print("Part time: ", "\n Daily:$", str(hourlywage*4), "\n Weekly:$", str(hourlywage*20), "\n Yearly:$", str(hourlywage*1040))
