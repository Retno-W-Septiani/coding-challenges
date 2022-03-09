# the words:
string = ('hi', 'dee', 'hi', 'how', 'are', 'you', 'mr', 'dee')
# print(string)
#this one is only the counts
for i in string:
   print(string.count(i))

#found this method on the internet:
frequency = {}
for i in string:
    if i in frequency:
       frequency[i.lower()] = frequency[i.lower()] + 1
    else:
        frequency[i.lower()] = 1
print(frequency)
