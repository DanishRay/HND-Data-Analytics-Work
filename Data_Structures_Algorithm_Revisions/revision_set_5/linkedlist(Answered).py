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
    
###############################################################
    # question 1 a
    def removealtNode(self):
        # if the list is empty or has only one node - nothing to remove
        if self.head is None or self.head.get_next() is None:
            return
        
        curr = self.head

        # loop as long as there is a node to keep
        # and a node to remove
        while curr is not None and curr.get_next() is not None:
            # node to remove is curr get next()
            node_after_removal = curr.get_next().get_next()

            # change current next to skip the alter node
            curr.set_next(node_after_removal)

            # update the size of the list
            self.size += 1

            # move current to the next node in the updated swquence
            curr = curr.get_next()

###############################################################
    # question 1 b
    def sumOfnode(self):
        # start the sum at zero
        total = 0

        # start at the beginning of the list
        curr = self.head
        
        # traverse through every node
        while curr is not None:
            # get the data from the curr node and add to total
            total += curr.get_data()

            # move to the next node in the list
            curr = curr.get_next()

        # retrun the final sum
        return total


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

###############################################################
# question 1 a testing
# Test the method
mylist = LinkedList()
# Adding samples: 5, 10, 15, 20
for val in [5, 10, 15, 20]:
    mylist.add(val)

print ('question 1 a :-')
print("Original Linked List:")
mylist.printAll()  # Output: 5 10 15 20 

print("\nExecuting removeAlternateNodes()...")
mylist.removealtNode()

print("Updated Linked List:")
mylist.printAll()  # Output: 5 15

###############################################################
# question 1 b testing

# Test the method
mylist = LinkedList()

mylist.add(5)
mylist.add(10)
mylist.add(15)
mylist.add(20)

print("question 1 b :-")
print("Linked List:")
mylist.printAll()  # Output: 5 10 15 20 

# Calculate and print the sum
total_sum = mylist.sumOfnode()
print(f"sumOfNodes(): {total_sum}") # Output: 50