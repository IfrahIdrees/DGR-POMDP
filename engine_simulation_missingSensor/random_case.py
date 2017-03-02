from random import randint


return_value = []
number_sheet = [1, 2, 4, 8]
for x in number_sheet:
    #number = 2^x
    print "this number is", x
    for z in range(1, 5):
        this_case = []
        for y in range(1, x+1): 
            print "this y is", y
            this_case.append(randint(1, 19))
        return_value.append(this_case)


print return_value

