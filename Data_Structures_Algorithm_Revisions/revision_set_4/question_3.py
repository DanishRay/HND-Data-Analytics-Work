# question 3 a
def findMode(arr):
    # handle empty list case
    if not arr:
        return 'list is empty'
    
    # dictionary to store the freq of each number
    counts = {}

    for num in arr:
        if num in counts:
            counts[num] += 1
        else:
            counts[num] = 1


    # find the number with the highest freq
    mode_value = arr[0]
    max_counts = 0

    for num, count in counts.items():
        if count > max_counts:
            max_counts = count
            mode_value = num

    return mode_value

# testing
my_list = [1, 3, 4, 3, 2, 1, 3, 5, 3]
result = findMode(my_list)

print ('question 3 a :-')
print("List:", my_list)
print("The mode is:", result)


# question 3 b
def bubblesortwthcount(arr):
    n = len(arr)
    # initialize the comparison counter
    comparison_count = 0

    # outer loop for each pass
    for i in range(n):
        # inner loop for adjacent comparisons
        for j in range(0, n - i - 1):

            # increment count every time comparing two elements
            comparison_count += 1

            if arr[j] > arr[j + 1]:
                # swapping if its in the wrong order
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr, comparison_count

# testing
data = [64, 34, 25, 12, 22, 11, 90]
print ('question 3 b :-')
print("Original List:", data)

sorted_list, total_comparisons = bubblesortwthcount(data)

print("Sorted List:  ", sorted_list)
print("Total Comparisons Made:", total_comparisons)

###############################################################
# question 3 c
def differEvenOdd(arr):
    # initialize the counters
    even_sum = 0
    odd_sum = 0

    # loop through each number in the list
    for num in arr:
        # check if number is even
        if num % 2 ==0:
            even_sum += num
        else:
            odd_sum += num
    
    # calculate absolute difference
    result = abs (even_sum - odd_sum)   # abs() turns negative results into positive ones

    return result

# testing 
my_list = [1, 2, 3, 4, 5]
print ('question 3 c :- ')
print("List:", my_list)

output = differEvenOdd(my_list)
print("Output:", output)