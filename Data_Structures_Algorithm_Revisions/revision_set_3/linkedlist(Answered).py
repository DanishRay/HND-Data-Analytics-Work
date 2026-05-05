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
    
#################################################################
    # question 1 a
    def insertbeforevalue(self, target, newvalue):
        # checking if list is empty
        if self.is_empty():
            print ('list is empty')
            return

        # check if the target is the head
        if self.head.get_data() == target :
            new_node = Node(newvalue)
            new_node.set_next(self.head)
            self.head = new_node
            self.size += 1
            return
        
        # search through the list
        current = self.head
        previous = None

        while current is not None:
            if current.get_data() == target:
                new_node = Node(newvalue)
                new_node.set_next(current)
                previous.set_next(new_node)
                self.size += 1
                return
            
            previous = current
            current = current.get_next()

        print (f'target {target} not found')

#################################################################
    # question 1 b
    def reverselist(self):
        prev = None
        current = self.head

        # traverse the list and flip pointers
        while current is not None:
            next_node = current.get_next() # save the next node
            current.set_next(prev)         # point current node backwards
            prev = current                 # move prev to current
            current = next_node            # move current to next node

        # update the head of the list to the last node found
        self.head = prev


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

#################################################################
# question 1 a testing
# Setup
mylist = LinkedList()
mylist.add(10)
mylist.add(20)
mylist.add(30)
mylist.add(40)

print("question 1 a | Linked List:", end=" ")
mylist.printAll() # [10, 20, 30, 40]

# Action
print("question 1 a | insertBeforeValue(30, 25):", end=" ")
mylist.insertbeforevalue(30, 25)
mylist.printAll() # [10, 20, 25, 30, 40]

#################################################################
# question 1 b testing
# 1. Create the list
mylist = LinkedList()
mylist.add(1)
mylist.add(2)
mylist.add(3)
mylist.add(4)

print("question 1 b | Linked List:", end=" ")
mylist.printAll() 

# 2. Reverse it
print("question 1 b | reverseList():", end=" ")
mylist.reverselist()
mylist.printAll()