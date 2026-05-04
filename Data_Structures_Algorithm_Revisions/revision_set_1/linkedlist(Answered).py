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
    
    ##################################################################3
    # question 1 a
    # swapfirstandlast
    def swapFirstandLast(self):
        # checking if the list has fewer than 2 nodes
        if self.head is None or self.head.get_next() is None:
            print ('swapFirstandLast(): List has fewer than 2 nodes')
            return
        
        # if there are exactly 2 nodes
        if self.head.get_next().get_next() is None:
            first = self.head
            last = self.head.get_next()

            last.set_next(first)
            first.set_next(None)
            self.head = last
            return
        
        # if there are more than 2 nodes
        first = self.head
        penultimate = None
        last  = self.head

        # traverse to find the last and second to last nodes
        while last.get_next() is not None:
            penultimate = last
            last = last.get_next()

        # re-link the nodes
        last.set_next(first.get_next()) # last now points to the second node
        penultimate.set_next(first) # second to last now points to the old first
        first.set_next(None) # old first now points to nothing
        self.head = last # head now points to the old last

    ##################################################################
    # question 1 b
    def removeduplicates(self):
        # handles empty list case
        if self.head is None:
            print ('removeduplicates() : list is empty')
            return
        
        current = self.head

        # traverse until the end of the list
        while current.get_next() is not None:
            # comparing current node data with next node data
            if current.get_data() == current.get_next().get_data():
                # duplcate found - skip the next node
                new_next = current.get_next().get_next()
                current.set_next(new_next)
                self.size -= 1 # decrement size since a node is removed

            else:
                # no duplicate, move to the next node
                current = current.get_next()
        


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

##################################################################
# question 1 a testing
# Testing with multiple nodes
mylist = LinkedList()
for val in [10, 20, 30, 40]:
    mylist.add(val) 

print("Linked List:", end=" ")
mylist.printAll() 

mylist.swapFirstandLast()
print("swapFirstandLast():", end=" ")
mylist.printAll()

# Testing with 1 node
single_list = LinkedList()
single_list.add(10)
print("\nLinked List:", end=" ")
single_list.printAll()
single_list.swapFirstandLast()

##################################################################
# question 1 b testing
# Create the list and add sorted values
mylist = LinkedList()
for val in [1, 1, 2, 3, 3, 4]:
    mylist.add(val)

print("Linked List:", end=" ")
mylist.printAll() 

# Remove duplicates
mylist.removeduplicates()

print("removeduplicates():", end=" ")
mylist.printAll()

# Testing empty list
empty_list = LinkedList()
empty_list.removeduplicates()