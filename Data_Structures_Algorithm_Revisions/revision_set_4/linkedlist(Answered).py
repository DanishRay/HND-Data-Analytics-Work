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
    
##############################################################
    # question 1 a
    def deleteNthNode(self, n):
        # check if n is out of range
        if n < 1 or n > self.size:
            print (f'position {n} is invalid for a list of size {self.size}')
            return
        
        current = self.head

        # case - deleting the first node (1-based)
        if n == 1:
            self.head = current.get_next()
        else : 
            # case - deleting middle or last node
            # need to stop at the (n-1) node
            prev = None
            count = 1
            while count < n:
                prev = current
                current = current.get_next()
                count += 1

            # skip the nth node by linking previous to current next
            prev.set_next(current.get_next())

        # reduce size and confirm
        self.size -= 1
        print (f'node at position {n} deleted')

##############################################################
    # question 1 b
    def findmidvalue(self):
        # if the list is empty, there is no middle
        if self.head is None:
            return 'list is empty'
        
        # start both pointers at the head
        slow = self.head
        fast = self.head

        # move fast twice as fast as slow
        # to get the first middle in an even list
        # checking if fast.next and fast.next.next exist
        while fast.get_next() is not None and fast.get_next().get_next() is not None:
            slow = slow.get_next()
            fast = fast.get_next().get_next()

        # slow is now at the mid
        return slow.get_data()


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

##############################################################
# question 1 a testing
# Testing logic
test_list = LinkedList()
# Adding elements: 10, 20, 30, 40, 50
for val in [10, 20, 30, 40, 50]:
    test_list.add(val)

print("Original List:")
test_list.printAll()  # Expected: 10 20 30 40 50 

print("\nDeleting 3rd node (30)...")
test_list.deleteNthNode(3)

print("List after deletion:")
test_list.printAll()  # Expected: 10 20 40 50

##############################################################
# question 1 b testing
# Create the list and add items
mylist = LinkedList()
for i in [1, 2, 3, 4, 5]:
    mylist.add(i)

print("Linked List Content:")
mylist.printAll() 

middle = mylist.findmidvalue()
print("Middle Value:", middle) # Output: 3