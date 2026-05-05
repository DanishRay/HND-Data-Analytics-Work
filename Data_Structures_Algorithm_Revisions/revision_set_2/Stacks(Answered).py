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
    
#############################################################
    # question 2 a
    def duplicatetop(self):
        # check if the stack is empty
        if self.is_empty():
            return 'stack is empty'
        
        # get the current top item
        top_item = self.peek()

        # push the same item back onto the stack
        self.push(top_item)


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

###########################################################
# question 2 a testing
# Create the stack
my_stack = Stacks()

# Add initial elements: [20, 30, 40]
my_stack.push(20)
my_stack.push(30)
my_stack.push(40)

print("Stack before duplication:")
my_stack.printStack() # bottom to top: [20, 30, 40]

# Duplicate the top
my_stack.duplicatetop()

print("Stack after duplicateTop():")
my_stack.printStack() # bottom to top: [20, 30, 40, 40]
