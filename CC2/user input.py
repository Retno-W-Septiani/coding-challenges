age = int(input("Enter Age :"))

# condition
if 65 - age > 0:
    status = "keep working yo!"
else:
    status = "yeah, it's time to retire"
print("You have ", 65-age, "years left until retirement,", status)
