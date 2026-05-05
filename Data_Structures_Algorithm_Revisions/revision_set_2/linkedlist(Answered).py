class Node:
    def __init__(self, init_data):
        self.data = init_data
        self.next = None

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next

    def set_data(self, new_data):
        self.data = new_data

    def set_next(self, new_next):
        self.next = new_next


class LinkedList:
    def __init__(self):
        self.head = None   
        self.size = 0  

    def is_empty(self):
        return self.head is None

    # def add(self, item):
    #     temp = Node(item)
    #     temp.set_next(self.head)
    #     self.head = temp
    #     self.size += 1  

    #add for sorted list
    def add(self, item):
        new_node = Node(item)
        current = self.head
        previous = None

        # Find the correct position for the new node
        while current is not None and current.get_data() < item:
            previous = current
            current = current.get_next()

        if previous is None:
            # Insert at the beginning
            new_node.set_next(self.head)
            self.head = new_node
        else:
            # Insert between previous and current
            new_node.set_next(current)
            previous.set_next(new_node)

        self.size += 1


    def search(self, item):
        current = self.head
        found = False
        while current is not None and not found:
            if current.get_data() == item:
                found = True
            else:
                current = current.get_next()
        return found

    def remove(self, item):
        current = self.head
        previous = None
        while current is not None:
            if current.get_data() == item:
                if previous is None:  
                    self.head = current.get_next()
                else:  
                    previous.set_next(current.get_next())
                self.size -= 1 
                return f"{item} was removed"
            else:
                previous = current
                current = current.get_next()
        return "No item found"

    def printAll(self):
        current = self.head
        while current is not None:
            print(current.get_data(), end=" ")
            current = current.get_next()
        print()  

    def get_size(self):
        return self.size 
    
#######################################################################
    # question 1 a
    def movemaxtoend(self):
        # handle empty
        if self.head is None or self.head.get_next() is None:
            return
        
        # initialize pointers
        current = self.head
        prev = None

        max_node = self.head
        prev_to_max = None
        tail = self.head

        # traverse to find the max node and the tail
        while current is not None:
            if current.get_data() > max_node.get_data():
                max_node = current
                prev_to_max = prev

            # keep track of the last node
            if current.get_next() is None:
                tail = current

            prev = current
            current = current.get_next()

        # if max is already at the end, just stop
        if max_node ==tail:
            return
        
        # remove max_node from its current position
        if max_node ==self.head:
            # if max is at the start, move the head pointer forward
            self.head = self.head.get_next()
        else:
            # link the node before max to the node after max
            prev_to_max.set_next(max_node.get_next())
        
        # attach max_node to the end
        tail.set_next(max_node)
        max_node.set_next(None) # max is now the new tail

#######################################################################
    # question 1 b
    def countgreaterthan(self, value):
        # start a counter at zero
        count = 0

        # start at the beginnig of the list
        current = self.head

        # traverse until the end of the list
        while current is not None:
            # check if the data is greater than the given value
            if current.get_data() > value:
                count += 1

            # move to the next node
            current = current.get_next()

        # return the final tally
        return count



# Example Usage
mylist = LinkedList()
mylist.add(31)
mylist.add(77)
mylist.add(17)
mylist.add(93)
mylist.add(26)
mylist.add(54)  
mylist.add(77)  

mylist.printAll()  # Print all elements in the list
print("Size of the list:", mylist.get_size())  # Output the size
print("Search for 17:", mylist.search(17))  # Search for an element
print("Remove 77:", mylist.remove(77))  # Remove an element
mylist.printAll()  # Print all elements after removal
print("Is the list empty?", mylist.is_empty())  # Check if the list is empty

#######################################################################
# question 1 a testing
test_list = LinkedList()

# Manual insertion to match sample: [5, 10, 3, 8]
n1 = Node(5)
n2 = Node(10)
n3 = Node(3)
n4 = Node(8)
test_list.head = n1
n1.set_next(n2)
n2.set_next(n3)
n3.set_next(n4)

print("Linked List before:")
test_list.printAll() # Expected: 5 10 3 8 

test_list.movemaxtoend()

print("moveMaxToEnd() result:")
test_list.printAll() # Expected: 5 3 8 10

#######################################################################
# question 1 b testing
mylist = LinkedList()
mylist.add(1)
mylist.add(5)
mylist.add(7)
mylist.add(9)

print("Linked List:", end=" ")
mylist.printAll() 

# Test the new method
result = mylist.countgreaterthan(5)
print(f"countGreaterThan(5): {result}")