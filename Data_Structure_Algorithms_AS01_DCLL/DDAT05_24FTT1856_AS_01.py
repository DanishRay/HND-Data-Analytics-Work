import sys

class Node: ## Act as the bluepritn for everry single element in list
    def __init__(self, data):
        self.data = data ## Stores the actual value (number / strings)
        self.next = None ## A pointer that will eventually store the address of the next node
        self.prev = None ## A pointer that will store the address of the previous node (What make it doubly linked)

class DoublyCircularLinkedList:
    def __init__(self, limit):
        self.head = None
        self.limit = limit  # Maximum allowed items
        self.count = 0      # Current number of items

    ## ADD ITEM ##
    def add(self, item):
        if self.count >= self.limit:
            return False

        new_node = Node(item)
        
        if not self.head:
            # The base case: point to itself
            new_node.next = new_node.prev = new_node
            self.head = new_node
        else:
            # Standard logic: Works for 1 node or 100 nodes
            tail = self.head.prev
            new_node.next = self.head
            new_node.prev = tail
            tail.next = self.head.prev = new_node

        self.count += 1
        return True
    
    def display(self):
        if not self.head:
            print("List is empty.")
            return
        
        nodes = []
        curr = self.head
        for _ in range(self.count):
            nodes.append(str(curr.data))
            curr = curr.next
        print(" <-> ".join(nodes) + " <-> (back to head)")
        ## Since there is no [None] at the end of the list, using the [count] is to know exavtly when to stop looping

    ## DELETE BY INDEX ##
    def delete_by_index(self, index):
        ## Validation: Check if index is within bounds
        if index < 0 or index >= self.count:
            print(f"Index {index} is out of range.")
            return False

        ## Travel to the node at the specified index
        curr = self.head
        
        ## Optimization: If index is in the second half, walk backwards!
        if index < self.count // 2:
            for _ in range(index):
                curr = curr.next
        else:
            for _ in range(self.count - index):
                curr = curr.prev

        ## Case: Deleting the only node
        deleted_data = curr.data # Grab the data before unlinking
        
        if self.count == 1:
            self.head = None
        else:
            curr.prev.next = curr.next
            curr.next.prev = curr.prev
            if index == 0:
                self.head = curr.next

        self.count -= 1
        curr.next = curr.prev = None 
        print(f"Deleted item at index {index}. New size: {self.count}")
        
        return deleted_data # Return the value to the user

    ## DELETE RANGE ##
    def delete_range(self, start_idx, end_idx):
        if not self.head or start_idx < 0 or end_idx >= self.count or start_idx > end_idx:
            return False

        # 1. Traverse to start
        start_node = self.head
        for _ in range(start_idx):
            start_node = start_node.next
        
        # 2. Traverse to end
        end_node = start_node
        for _ in range(end_idx - start_idx):
            end_node = end_node.next

        # 3. The "Universal Stitch"
        before = start_node.prev
        after = end_node.next
        before.next = after
        after.prev = before

        # 4. Update Head & Counter
        if start_idx == 0:
            self.head = None if self.count == (end_idx - start_idx + 1) else after

        self.count -= (end_idx - start_idx) + 1
        return True
    
    ## DELETE ITEM ##
    def delete(self, item):
        if not self.head:
            return False

        # 1. Find the node 
        curr = self.head
        for _ in range(self.count):
            if curr.data == item:
                break
            curr = curr.next
        else: # This 'else' belongs to the 'for' loop; it runs if no 'break' happened
            print(f"Item '{item}' not found.")
            return False

        # 2. The Stitch
        curr.prev.next = curr.next
        curr.next.prev = curr.prev

        # 3. Update the Head pointer.
        if curr == self.head:
            self.head = curr.next if self.count > 1 else None

        # 4. Finalize
        self.count -= 1
        print(f"Deleted: {item}. (Size: {self.count})")
        return True
    
    ## REVERSED ##
    def reverse(self):
        if not self.head:
            return

        curr = self.head
        for _ in range(self.count):
            curr.next, curr.prev = curr.prev, curr.next
            curr = curr.prev 

        self.head = self.head.next

    ## SEARCH BY INDEX ##
    def search_by_index(self, index):
        if not (0 <= index < self.count):
            return None

        # Determine direction and distance
        is_forward = index < self.count // 2
        steps = index if is_forward else (self.count - index)
        direction = "next" if is_forward else "prev"

        # Single loop regardless of direction
        curr = self.head
        for _ in range(steps):
            curr = getattr(curr, direction)

        return curr.data
    
    ## SEARCH ITEM ##
    def search(self, item):
        if not self.head:
            return -1

        curr = self.head
        # Using a loop based on count to ensure we check every node exactly once
        for i in range(self.count):
            if curr.data == item:
                return i  # Return the position where it was found
            curr = curr.next

        return -1  # Item was not in the list
    
    ## SET SIZE LIMIT ##
    def set_size_limit(self, new_limit):
        # Use max to ensure the limit is at least 0
        self.limit = max(0, new_limit)
        
        # Optional: Log the change
        status = "overflowing" if self.count > self.limit else "active"
        print(f"Limit updated to {self.limit}. List status: {status}")
        
        return self.limit

    ## Allowing to use " len(list) " ##
    def __len__(self):
        return self.count


## TESTING FOR ADD_ITEM ##
def run_simulation_add():
    # Initialize list with a limit of 5
    my_list = DoublyCircularLinkedList(limit=5)
    print("--- DCLL ADDITION SIMULATION ---")

    # 1. Add item to empty list
    print("\n1. Testing: Add to empty list")
    my_list.add(10) #
    my_list.display() # Should show: 10 <-> (back to head)

    # 2. Add item to a list with existing elements (Tail Position)
    print("\n2. Testing: Add to list with existing elements (Tail)")
    my_list.add(20) #
    my_list.add(30) #
    my_list.display() # Should show: 10 <-> 20 <-> 30

    # 3. Add items at the head position
    # To add at the head in your current logic, we add normally and then re-assign head
    print("\n3. Testing: Add at the head position")
    my_list.add(5) # Adds to tail first
    my_list.head = my_list.head.prev # Shift head pointer to the new node
    my_list.display() # Should show: 5 <-> 10 <-> 20 <-> 30

    # 4. Add items to a full list
    print("\n4. Testing: Add items to a full list")
    my_list.add(40) # List is now at limit (5/5)
    result = my_list.add(50) # Attempting 6th item
    if not result:
        print("Blocked: Successfully prevented adding to a full list.")

    # 5. Items added are sorted (Visual Check)
    print("\n5. Testing: Verify sorted order")
    # Current list: 5, 10, 20, 30, 40
    my_list.display()

    # 6. Verify list integrity (Check all items via forward and backward links)
    print("\n6. Testing: List Integrity (Forward & Backward)")
    head_node = my_list.head
    tail_node = head_node.prev #
    print(f"Head: {head_node.data}")
    print(f"Tail (Head.prev): {tail_node.data}")
    print(f"Tail.next: {tail_node.next.data} (Should be Head)")

## TESTING FOR DELETE_ITEM ##
def run_simulation_delete():
    # Setup: Initialize list with 5 items for testing
    my_list = DoublyCircularLinkedList(limit=10)
    for x in [10, 20, 30, 40, 50]:
        my_list.add(x)
    
    print("\n--- DCLL DELETION SIMULATION ---")
    print("Initial List:")
    my_list.display()

    # 1. Delete item at the head
    print("\n1. Testing: Delete item at the head (10)")
    my_list.delete(10) #
    my_list.display() # Expected: 20 <-> 30 <-> 40 <-> 50

    # 2. Delete item at middle position
    print("\n2. Testing: Delete item at middle position (30)")
    my_list.delete(30) #
    my_list.display() # Expected: 20 <-> 40 <-> 50

    # 3. Delete item at tail position
    print("\n3. Testing: Delete item at tail position (50)")
    my_list.delete(50) #
    my_list.display() # Expected: 20 <-> 40

    # 4. Delete item that is not in the list
    print("\n4. Testing: Delete item not in list (99)")
    result = my_list.delete(99) #
    if not result:
        print("Result: Correctly identified item not found.")

    # 5. Verify list integrity
    print("\n5. Testing: Verify list integrity (Check 20 <-> 40 circularity)")
    print(f"Current Head: {my_list.head.data}")
    print(f"Head.next: {my_list.head.next.data} (Should be 40)")
    print(f"Head.prev: {my_list.head.prev.data} (Should be 40)")

    # 6. Delete items until one remains, then delete last item
    print("\n6. Testing: Delete until one remains, then delete last")
    my_list.delete(40)
    print("One item left:")
    my_list.display()
    my_list.delete(20) # Deleting the only node
    my_list.display()

    # 7. Delete items from an empty list
    print("\n7. Testing: Delete from an empty list")
    result = my_list.delete(100) #
    if not result:
        print("Result: Correctly blocked deletion from empty list.")

## TESTING FOR DELETE_RANGE ##
def run_simulation_delete_range():
    # Setup: Initialize list with 6 items (Indices 0-5)
    my_list = DoublyCircularLinkedList(limit=10)
    for x in ["A", "B", "C", "D", "E", "F"]:
        my_list.add(x)
    
    print("\n--- DCLL DELETE RANGE SIMULATION ---")
    print("Initial List:")
    my_list.display() # A, B, C, D, E, F

    # 1. Delete items within a specified range (Middle)
    print("\n1. Testing: Delete range in middle (Indices 1 to 2: 'B', 'C')")
    my_list.delete_range(1, 2)
    my_list.display() # Expected: A <-> D <-> E <-> F

    # 2. Delete range that includes the Head (Index 0)
    print("\n2. Testing: Delete range starting at Head (Indices 0 to 1: 'A', 'D')")
    # Current list is A, D, E, F
    my_list.delete_range(0, 1)
    my_list.display() # Expected: E <-> F

    # 3. Handle scenarios where the range overlaps with the end of the list
    # Let's reset the list to test a full tail-end deletion
    print("\n3. Testing: Delete range reaching the end of the list")
    my_list = DoublyCircularLinkedList(limit=10)
    for x in [1, 2, 3, 4, 5]: my_list.add(x)
    # List: 1, 2, 3, 4, 5. Delete 3, 4 (Indices 2 to 3)
    my_list.delete_range(2, 3)
    my_list.display() # Expected: 1 <-> 2 <-> 5

    # 4. Validate list structure and integrity after bulk deletion
    print("\n4. Testing: Verify list integrity (Check 1 <-> 2 <-> 5 circularity)")
    head = my_list.head
    tail = head.prev
    print(f"New Head: {head.data}")
    print(f"New Tail: {tail.data}")
    print(f"Tail.next points to: {tail.next.data} (Should be Head: 1)")
    print(f"Head.prev points to: {head.prev.data} (Should be Tail: 5)")

    # 5. Delete everything (Whole range)
    print("\n5. Testing: Delete entire range (Indices 0 to 2)")
    my_list.delete_range(0, 2)
    my_list.display() # Expected: List is empty

## TESTING FOR DELETE_BY_INDEX ##
def run_simulation_delete_by_index():
    # Setup: Initialize list with 5 items (Indices 0-4)
    my_list = DoublyCircularLinkedList(limit=10)
    for x in ["Red", "Blue", "Green", "Yellow", "Purple"]:
        my_list.add(x)
    
    print("\n--- DCLL DELETE BY INDEX SIMULATION ---")
    print("Initial List:")
    my_list.display() # Red, Blue, Green, Yellow, Purple

    # 1. Delete item at negative index
    print("\n1. Testing: Delete item at negative index (-1)")
    result = my_list.delete_by_index(-1)
    if not result:
        print("Result: Correctly blocked negative index.")

    # 2. Delete item at index greater than the size
    print(f"\n2. Testing: Delete item at index out of bounds (Index 10, Size {my_list.count})")
    result = my_list.delete_by_index(10)
    if not result:
        print("Result: Correctly blocked out-of-bounds index.")

    # 3. Delete item at the head position (Index 0)
    print("\n3. Testing: Delete item at the head position (Index 0: 'Red')")
    my_list.delete_by_index(0)
    my_list.display() # Expected: Blue <-> Green <-> Yellow <-> Purple
    print(f"New Head: {my_list.head.data}") # Should be 'Blue'

    # 4. Delete item at the tail position
    # Remaining: Blue (0), Green (1), Yellow (2), Purple (3)
    last_idx = my_list.count - 1
    print(f"\n4. Testing: Delete item at the tail position (Index {last_idx}: 'Purple')")
    my_list.delete_by_index(last_idx)
    my_list.display() # Expected: Blue <-> Green <-> Yellow

    # 5. Verify list integrity after deletion
    print("\n5. Testing: Verify list integrity (Check Blue <-> Green <-> Yellow)")
    head = my_list.head
    tail = head.prev
    print(f"Current Head: {head.data}")
    print(f"Current Tail: {tail.data}")
    # Check circularity
    print(f"Tail.next points to: {tail.next.data} (Should be Head: Blue)")
    print(f"Head.prev points to: {head.prev.data} (Should be Tail: Yellow)")

## TESTING FOR SEARCH_ITEM ##
def run_simulation_search():
    # Initialize list with a limit of 10
    my_list = DoublyCircularLinkedList(limit=10)
    
    print("\n--- DCLL SEARCH SIMULATION ---")

    # 1. Search for an item in an empty list
    print("1. Testing: Search in an empty list")
    index = my_list.search("Apple")
    print(f"Result for 'Apple': {index} (Expected: -1)")

    # Setup: Add items for further testing
    # List: ["Red", "Blue", "Green", "Blue", "Yellow"]
    for x in ["Red", "Blue", "Green", "Blue", "Yellow"]:
        my_list.add(x)
    print("\nInitial List for searching:")
    my_list.display()

    # 2. Search for item that exists in the list
    print("\n2. Testing: Search for existing item ('Green')")
    index = my_list.search("Green")
    print(f"Item 'Green' found at index: {index} (Expected: 2)")

    # 3. Search for item that does not exist
    print("\n3. Testing: Search for non-existent item ('Purple')")
    index = my_list.search("Purple")
    print(f"Item 'Purple' found at index: {index} (Expected: -1)")

    # 4. Search for multiple occurrences of an item
    print("\n4. Testing: Search for multiple occurrences ('Blue')")
    print("Note: The current implementation returns the index of the FIRST occurrence.")
    index = my_list.search("Blue")
    print(f"First 'Blue' found at index: {index} (Expected: 1)")

    # 5. Verify search after list modification
    print("\n5. Testing: Search after deleting an item")
    my_list.delete("Red") # "Blue" (prev index 1) should now be at index 0
    my_list.display()
    index = my_list.search("Blue")
    print(f"New index for 'Blue': {index} (Expected: 0)")

## TESTING FOR SEARCH_BY_INDEX ##
def run_simulation_search_by_index():
    # Setup: Initialize list with 5 items
    # Indices: 0: "Mercury", 1: "Venus", 2: "Earth", 3: "Mars", 4: "Jupiter"
    my_list = DoublyCircularLinkedList(limit=10)
    planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter"]
    for p in planets:
        my_list.add(p)
    
    print("\n--- DCLL SEARCH BY INDEX SIMULATION ---")
    my_list.display()

    # 1. Search for item by a negative index
    print("\n1. Testing: Search for negative index (-1)")
    result = my_list.search_by_index(-1)
    print(f"Result for index -1: {result} (Expected: None)")

    # 2. Search for item that exists (First Half - Forward Search)
    print("\n2. Testing: Search for existing item at Index 1 (Forward)")
    result = my_list.search_by_index(1)
    print(f"Result for index 1: {result} (Expected: Venus)")

    # 3. Search for item that exists (Second Half - Backward Search)
    # This triggers the 'prev' optimization in your code
    print("\n3. Testing: Search for existing item at Index 4 (Backward)")
    result = my_list.search_by_index(4)
    print(f"Result for index 4: {result} (Expected: Jupiter)")

    # 4. Search for item at index greater than the size of the list
    print(f"\n4. Testing: Search for out-of-bounds index (Index 10, Size {len(my_list)})")
    result = my_list.search_by_index(10)
    print(f"Result for index 10: {result} (Expected: None)")

    # 5. Search in an empty list
    empty_list = DoublyCircularLinkedList(limit=5)
    print("\n5. Testing: Search by index in an empty list")
    result = empty_list.search_by_index(0)
    print(f"Result for index 0 in empty list: {result} (Expected: None)")

## TESTING FOR SIZE LIMIT ##
def run_simulation_size_limit():
    print("\n--- DCLL SIZE LIMIT SIMULATION ---")

    # 1. Check size limit of a new initialized list
    initial_limit = 3
    my_list = DoublyCircularLinkedList(limit=initial_limit)
    print(f"1. New list initialized with limit: {my_list.limit} (Expected: 3)")
    print(f"   Current count: {my_list.count} (Expected: 0)")

    # 2. Check size after setting a new limit
    print("\n2. Testing: Update limit before adding items")
    my_list.set_size_limit(5)
    print(f"   New limit: {my_list.limit} (Expected: 5)")

    # 3. Check size after exceeding the new limit
    print("\n3. Testing: Fill list and attempt to exceed limit")
    # Fill to 5/5
    for i in range(5):
        my_list.add(f"Item {i}")
    
    print(f"   List count: {my_list.count}/{my_list.limit}")
    
    # Attempt to add the 6th item
    added = my_list.add("Overhead Item")
    if not added:
        print("   Success: Addition blocked at limit 5.")
    print(f"   Final count: {my_list.count} (Expected: 5)")

    # 4. Check size limit after changing the limit multiple times
    print("\n4. Testing: Multiple limit changes")
    
    # Increase limit
    my_list.set_size_limit(10)
    my_list.add("Extra Item")
    print(f"   Limit increased to 10. Current count: {my_list.count} (Expected: 6)")
    
    # Decrease limit below current count
    # Note: Your set_size_limit only changes the attribute; it doesn't delete nodes.
    my_list.set_size_limit(2)
    print(f"   Limit decreased to 2. Current count: {my_list.count}")
    
    # Verify that adding is now blocked because count (6) > limit (2)
    blocked_add = my_list.add("New Item")
    if not blocked_add:
        print("   Success: Adding blocked because list is 'overflowing' the new small limit.")

## TESTING FOR SET_SIZE_LIMIT ##
def run_simulation_set_limit_scenarios():
    # Initialize list with 3 items
    my_list = DoublyCircularLinkedList(limit=10)
    for x in ["A", "B", "C"]:
        my_list.add(x)
    
    print("\n--- DCLL SET_SIZE_LIMIT SCENARIOS ---")
    print(f"Initial State: Count={my_list.count}, Limit={my_list.limit}")

    # 1. Set size limit to a positive number
    print("\n1. Testing: Set limit to positive number (15)")
    my_list.set_size_limit(15)
    print(f"   Result: Limit is now {my_list.limit} (Expected: 15)")

    # 2. Set size limit to zero or negative number
    print("\n2. Testing: Set limit to negative number (-5)")
    my_list.set_size_limit(-5)
    print(f"   Result: Limit is now {my_list.limit} (Expected: 0 due to max(0, new_limit))")
    
    # 3. Set size limit smaller than the current size of the list
    print("\n3. Testing: Set limit (2) smaller than current count (3)")
    my_list.set_size_limit(2)
    print(f"   Result: Limit={my_list.limit}, Count={my_list.count}")
    # Verify that we cannot add more, but the list still exists
    added = my_list.add("D")
    print(f"   Adding 'D' blocked? {not added} (Expected: True)")

    # 4. Set size limit larger than the current size of the list
    print("\n4. Testing: Set limit (10) larger than current count (3)")
    my_list.set_size_limit(10)
    print(f"   Result: Limit={my_list.limit}, Count={my_list.count}")
    # Verify that we can now add again
    added = my_list.add("D")
    print(f"   Adding 'D' successful? {added} (Expected: True)")
    my_list.display()

## TESTING FOR REVERSE ##
def run_simulation_reverse():
    print("\n--- DCLL REVERSE SIMULATION ---")
    
    # 1. Reverse a list containing duplicate and unique items
    my_list = DoublyCircularLinkedList(limit=10)
    # Setup: [10, 20, 10, 30] -> Mix of unique and duplicates
    for x in [10, 20, 10, 30]:
        my_list.add(x)
    
    print("Initial List:")
    my_list.display() # Expected: 10 <-> 20 <-> 10 <-> 30

    print("\n1 & 2. Testing: Reversing order with duplicates")
    my_list.reverse()
    my_list.display() # Expected: 30 <-> 10 <-> 20 <-> 10
    
    # 3. Verify the head and tail after reversal
    print("\n3. Testing: Verify Head and Tail Integrity")
    new_head = my_list.head
    new_tail = my_list.head.prev
    
    print(f"New Head: {new_head.data} (Expected: 30)")
    print(f"New Tail (Head.prev): {new_tail.data} (Expected: 10)")
    
    # Check circularity: Tail's next should be the new head
    print(f"Tail.next points to: {new_tail.next.data} (Should be 30)")
    
    # 4. Reverse an empty list (Boundary Case)
    empty_list = DoublyCircularLinkedList(limit=5)
    print("\n4. Testing: Reverse an empty list")
    empty_list.reverse()
    empty_list.display() # Expected: List is empty.
    
    # 5. Reverse a single-item list
    single_list = DoublyCircularLinkedList(limit=5)
    single_list.add("Only One")
    print("\n5. Testing: Reverse a single-item list")
    single_list.reverse()
    single_list.display() # Expected: Only One <-> (back to head)

## TESTING FOR SORTED INTEGRITY ##
def run_simulation_sorted_integrity():
    print("\n--- DCLL SORTED INTEGRITY SIMULATION ---")
    
    # 1. Items after insertion (Manually adding in sorted order)
    my_list = DoublyCircularLinkedList(limit=10)
    for x in [10, 20, 30, 40]:
        my_list.add(x)
    
    print("1. Initial Sorted List:")
    my_list.display() # Expected: 10 <-> 20 <-> 30 <-> 40

    # 2. Items remain sorted after deletion
    print("\n2. Testing: Sorted order after deleting middle item (20)")
    my_list.delete(20) #
    my_list.display() # Expected: 10 <-> 30 <-> 40
    # Verification: 10 < 30 < 40 is still sorted.

    # 3. Items remain sorted after searching
    print("\n3. Testing: Sorted order after searching for '40'")
    my_list.search(40) #
    my_list.display() # Expected: 10 <-> 30 <-> 40 (Search should not move nodes)

    # 4. Items remained "sorted" after reversing
    # Note: Reversing a sorted list results in a "Descending Sorted" list.
    print("\n4. Testing: Sorted order after reversing")
    my_list.reverse() #
    print("List after reverse (Should be Descending):")
    my_list.display() # Expected: 40 <-> 30 <-> 10

if __name__ == "__main__":
    run_simulation_add()
    run_simulation_delete()
    run_simulation_delete_range()
    run_simulation_delete_by_index()
    run_simulation_search()
    run_simulation_search_by_index()
    run_simulation_size_limit()
    run_simulation_set_limit_scenarios()
    run_simulation_reverse()
    run_simulation_sorted_integrity()