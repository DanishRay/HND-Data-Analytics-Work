class Stacks:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)
    
    def printStack(self):
        print("bottom to top:" , self.items)

    def reversePrintStack(self):
        print("Stack (top -> bottom):")
        for item in reversed(self.items):
            print(item)
    
################################################################
    # question 2 a
    def copystack(self):
        # create the two utility stacks
        copy_stack = Stacks()
        temp_stack = Stacks()

        # move items from self to temp
        while not self.is_empty():
            temp_stack.push(self.pop())

        # move items from temp to both self and copy_stack
        while not temp_stack.is_empty():
            item = temp_stack.pop()
            self.push(item)        # restore original stack
            copy_stack.push(item)  # build the copy stack
        
        return copy_stack


# Example Usage
new_stack = Stacks()

# Adding elements to the stack so that 6 is at the bottom
new_stack.push(1)
new_stack.push(2)
new_stack.push(3)
new_stack.push(4)

# Testing stack methods
print("Is stack empty?", new_stack.is_empty())
print("Top item:", new_stack.peek())
print("Stack size:", new_stack.size())
print("Popped item:", new_stack.pop())
print("Stack size after pop:", new_stack.size())
new_stack.printStack()
new_stack.reversePrintStack()

################################################################
# question 2 a testing
# setup original stack
original = Stacks()
original.push(30)
original.push(40)
original.push(50)

# display original
print("Original stack (top to bottom):", end=" ")
# Using a list comprehension to show items top-to-bottom for display
print([original.items[i] for i in range(len(original.items)-1, -1, -1)]) 

# create copy
cloned_stack = original.copystack()

# display copy
print("copyStack():", end=" ")
print([cloned_stack.items[i] for i in range(len(cloned_stack.items)-1, -1, -1)])