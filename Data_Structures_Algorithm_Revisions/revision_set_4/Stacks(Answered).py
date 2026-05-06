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

######################################################
    # question 2 a
    def reverseStack(self):
        # create the one allowed temporary stack
        temp_stack = Stacks()
        n = self.size()

        # loop through the stack
        for i in range(n):
            # pop the top element to hold it
            temp_val = self.pop()

            # move the remaining element that haven't been fixed yet
            # to the temp stack
            for _ in range(n - 1 - i):
                temp_stack.push(self.pop())

            # push the held element back
            self.push(temp_val)

            # move everything back from tempt to main
            while not temp_stack.is_empty():
                self.push(temp_stack.pop())
    

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

######################################################
# question 2 a
# Create stack and push items
s = Stacks()
for val in [1, 2, 3, 4]:
    s.push(val)

print('question 2 a :-')
print("Before Reverse:")
s.printStack() # Output: bottom to top: [1, 2, 3, 4]

# Perform reversal
s.reverseStack()

print("After Reverse:")
s.printStack() # Output: bottom to top: [4, 3, 2, 1]