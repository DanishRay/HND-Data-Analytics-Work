# question 3 a
def findthirdlargest(arr):
    # removing duplicates to ensure find the 3rd unique largest value
    unique_nums = list(set(arr))

    # check if have enough elements after removing duplicates
    if len(unique_nums) < 3:
        return 'fewer than 3 unique elements exist'
    
    # sort the list in descending order
    unique_nums.sort(reverse=True)

    # return the element at index 2
    return unique_nums[2]

# testing
# Test Case 1: Standard list
print ('question 3 a')
list1 = [10, 20, 30, 40]
print(f"List: {list1}")
print(f"Output: {findthirdlargest(list1)}") # Expected: 20

# Test Case 2: List with duplicates
list2 = [50, 50, 40, 30, 20]
print(f"List: {list2}")
print(f"Output: {findthirdlargest(list2)}") # Expected: 30

# Test Case 3: Too few elements
list3 = [10, 20]
print(f"List: {list3}")
print(f"Output: {findthirdlargest(list3)}")

#################################################################
# question 3 b
def insertionsorttracked(arr):
    comparisons = 0
    swaps = 0

    # start from the second elemnt
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # perform at least one comparison to check the while condition
        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]     # shift element
                swaps += 1              # count the shift/swap
                j -= 1
            else:
                # if the arr[j] <= key, the loop while loop will stop
                # but it is already counted the comparison above
                break
        
        # place the key in its correct position
        arr[j + 1] = key
    
    return arr, comparisons, swaps

# testing
print ('question 3 b')
data = [12, 11, 13, 5, 6]
print(f"Original List: {data}")

sorted_data, comp_count, swap_count = insertionsorttracked(data)

print(f"Sorted List:   {sorted_data}")
print(f"Comparisons:   {comp_count}")
print(f"Swaps/Shifts:  {swap_count}")

#################################################################
# question 3 c
def sumofsquares(arr):
    # initialize total to zero
    total = 0

    # iterate through each number in the provided list
    for num in arr:
        # square the number and add it to the total
        total += (num * num)

    return total

# testing
my_list = [2, 3, 4]
print ('question 3 c')
result = sumofsquares(my_list)

print(f"List: {my_list}")
print(f"Output: {result}")