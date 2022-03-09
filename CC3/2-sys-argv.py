import sys
print("This is income calculator")
hourlywage = int(input("Input hourly wage :"))

# condition
print("Full time: ", "\n Daily:$", str(hourlywage*8), "\n Weekly:$", str(hourlywage*40), "\n Yearly:$", str(hourlywage*2080))
print("Part time: ", "\n Daily:$", str(hourlywage*4), "\n Weekly:$", str(hourlywage*20), "\n Yearly:$", str(hourlywage*1040))
(sys.argv)