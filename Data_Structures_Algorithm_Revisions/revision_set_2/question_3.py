# question 3 a
def findmissingnum(arr):
    # find the starting point of the sequence
    start = min(arr)

    # find the ending point
    end = max(arr)

    # loop through the full range 
    for number in range(start, end + 1):
        # if the expected number is not in the array - its the missing one
        if number not in arr:
            return number
        
    return 'no number is missing'

# testing
my_list = [1, 2, 3, 5]
print("question 3 a List:", my_list)

result = findmissingnum(my_list)
print("question 3 a Output:", result)

##################################################################
# question 3 b
def bubblesort(arr):
    # initialize the pass counter
    pass_count = 0
    n = len(arr)

    # the outer loop represents each pass
    for i in range(n - 1):
        # assuming the list be sorted already
        swapped = False

        # inner loop - compares adjacent elements
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                # swap the elements
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        # increment the pass counter after the inner loop finishes
        pass_count += 1

    return pass_count

# testing 
original_list = [4, 3, 2, 1]
print("question 3 b | Original:", original_list)

# We make a copy to keep the original list for printing
test_list = original_list.copy()
total_passes = bubblesort(test_list)

print("question 3 b | Sorted:", test_list)
print("question 3 b | Total passes:", total_passes)

##################################################################
# question 3 c
def filternegative(arr):
    # create a new empty list to hold the positive numbers
    filtered_list = []

    # loop through every number in the provided array
    for number in arr:
        # check if the number is 0 or greater
        if number >= 0:
            # add the non-negative number to our new list
            filtered_list.append(number)
    
    # return the newly built list
    return filtered_list

# testing
original_list = [3, -2, 5, -1, 7]
print("question 3 c | List:", original_list)

result = filternegative(original_list)
print("question 3 c | Output:", result)