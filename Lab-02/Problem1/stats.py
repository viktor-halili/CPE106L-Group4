# Lee Programming Problem 1 Code 😃

def border():
    print("-------------------------------------------")


def number():
    size = int(input("How many numbers do you want?: "))
    list_of_numbers = []

    for x in range(1, size + 1):
        number = float(input(f"Please input number #{x}: "))  
        list_of_numbers.append(number)

    print(f"Your list is: {list_of_numbers}")
    return list_of_numbers


def list_checker(my_list):
    x = False
    while not x:
        i = input("Is your list correct? (y/n): ")

        if i.lower() == "y":
            border()
            x = True
        else:
            border()
            my_list = number()   
    return my_list


def mean(givenList):

    if givenList == []:
        return 0

    else:
        return sum(givenList) / len(givenList)


def median(givenList):
    sorted_list = sorted(givenList)      
    n = len(sorted_list)
    mid = n // 2

    if n % 2 == 0:  
        return (sorted_list[mid - 1] + sorted_list[mid]) / 2
    else:           
        return sorted_list[mid]




# main program
border()
nums = number()            
nums = list_checker(nums)  

checker = 0
while checker < 1:
    print("[1] mean \n")
    print("[2] median \n")

    j = input("Please pick which do you want to find: ")

    if j == "1":
        print("Mean is:", mean(nums))   
        border()
        checker = 1

    elif j == "2":
        print("Median is:", median(nums))  
        border()
        checker = 1

    else:
        checker = 0

border()