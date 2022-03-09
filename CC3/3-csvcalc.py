import csv

year_list, month_list, value_list = [], [], []

with open('co2-ppm-daily.csv') as co2:
    print(co2)
    csv_reader = csv.reader(co2, delimiter=',')
    line_count = 0
    header = next(csv_reader) #to skip the header
    print (header)

    for row in csv_reader:
        year, month, day = row[0].split('-') #splitting the date info into column /list
        # first data would be 1958-03-30
        if year not in year_list:
            year_list.append(year)
        if month not in month_list:
            month_list.append(month)
        value_list.append(float(row[1])) #using float to interpret the value as number
        line_count = line_count + 1

# Step 1
print('Minimum =' + str(min(value_list)))
print('Max =' + str(max(value_list)))
print('Average =' + str(sum(value_list)/ len(value_list)))

# Average for each year
print('We have: ' + str(len(year_list)) + 'years of data')
for year_select in year_list:
    co2_by_year = []
    with open('co2-ppm-daily.csv') as co2:
        csv_reader = csv.reader(co2, delimiter=',')
        line_count = 0
        header = next(csv_reader) #to skip the header
        print (header)

        for row in csv_reader:
            year, month, day = row[0].split('-')
            if year == year_select:
                co2_by_year.append(float(row[1]))

    print('year is:' + str(year_select) + ' co2 is:' + str(float(sum(co2_by_year) / len(co2_by_year))))

#seasonal value
print('seasonal co2 value')
winter = ['12', '01', '02']
spring = ['03', '04', '05']
summer = ['06', '07', '08']
autumn = ['09', '10', '11']

winter_co2 = []
spring_co2 = []
summer_co2 = []
autumn_co2 = []

with open('co2-ppm-daily.csv') as co2:
    csv_reader = csv.reader(co2, delimiter=',')
    line_count = 0
    header = next(csv_reader) #to skip the header

    for row in csv_reader:
        year, month, day = row[0].split('-')
        if month in winter:
            winter_co2.append(float(row[1]))
        if month in spring:
            spring_co2.append(float(row[1]))
        if month in summer:
            summer_co2.append(float(row[1]))
        if month in autumn:
            autumn_co2.append(float(row[1]))


print('winter co2 is:' + str(float(sum(winter_co2) / len(winter_co2))) + ' ppm')
print('spring co2 is:' + str(float(sum(spring_co2) / len(spring_co2))) + ' ppm')
print('summer co2 is:' + str(float(sum(summer_co2) / len(summer_co2))) + ' ppm')
print('autumn co2 is:' + str(float(sum(autumn_co2) / len(autumn_co2))) + ' ppm')

#Anomaly
overal_mean = str(sum(value_list)/ len(value_list))
print(overal_mean)

with open('co2-ppm-daily.csv') as co2:
    csv_reader = csv.reader(co2, delimiter=',')
    line_count = 0
    header = next(csv_reader) #to skip the header

    for row in csv_reader:
        print(float(str(row[1])) - float(overal_mean))
