# question 3

# question 3 a
def binarysearchcount(arr, target):
    # helper function to find the first or last occurrences
    def get_index(is_first):
        low, high = 0, len(arr) - 1
        result = -1
        while low <= high:
            mid = (low + high) //2
            if arr[mid] == target:
                result = mid
                if is_first:
                    high = mid -1 # look left for the start
                else:
                    low = mid +1 # look right for the mid
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid -1
        return result
    
    # get the boundaries
    first = get_index(True)

    # if the target isn't in the list at all
    if first == -1:
        return 0
    
    last = get_index(False)

    # total count calculation
    return last - first + 1

# testing 
my_list = [1, 2, 2, 3, 3, 3, 4]
target_val = 3

print("List:", my_list)
print("Target:", target_val)
print("Output:", binarysearchcount(my_list, target_val))


################################################################
# question 3 b
# selectionsort modify
def selectionsortwithswaps (arr):
    n = len(arr)
    swap_count = 0

    for i in range(n):
        # assume the current position is the smallest
        min_idx = i

        # check the rest of the list for a smaller value
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # only swap if a smaller element was found elsewhere
        if min_idx != i:
            arr [i], arr[min_idx] = arr[min_idx], arr[i]
            swap_count += 1

    return arr, swap_count

# testing 
original_list = [5, 4, 3, 2]
print("Original:", original_list)

sorted_list, total_swaps = selectionsortwithswaps(original_list[:])

print("Sorted:", sorted_list)
print("Swaps:", total_swaps)


################################################################
# question 3 c
def sumevennumbers(arr):
    # start total at zero
    total = 0

    # iterate through each number in the list
    for num in arr:
        # check if the number is even
        if num % 2 == 0:
            # add it to the total
            total += num
    
    # return the final sum
    return total

# testing
my_list = [1, 2, 3, 4, 6]
result = sumevennumbers(my_list)

print("List:", my_list)
print("Output:", result)