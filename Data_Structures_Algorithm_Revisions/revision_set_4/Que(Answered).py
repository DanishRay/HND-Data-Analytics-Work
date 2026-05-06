class Que:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []
    
    def enqueue(self, item):
        return self.items.insert(0,item) #insert to front

    def dequeue(self):
        return self.items.pop() #by default - pop remove the last item
    
    def removeAtIndex(self, index):
        self.items.pop(index)
          
    def size(self):
        return len(self.items)

    def printQueue(self):
        print(self.items)

############################################################
    # question 2 b
    def removeEverysec(self):
        # get the current size to know how many items to process
        initial_size = self.size()

        # iterate through all items currently in the queue
        for i in range(1, initial_size + 1):
            # dequeue the item at the front
            item = self.dequeue()

            # keep it - if it is an odd position
            if i % 2 != 0:
                self.enqueue(item)


myQueue = Que()

myQueue.enqueue(10)
myQueue.enqueue(20)
myQueue.enqueue(30)

print("Current Queue:")
myQueue.printQueue() 

print("Dequeued Element:", myQueue.dequeue())

print("Queue after dequeue:")
myQueue.printQueue()

print("Removing element at index 1:", myQueue.removeAtIndex(1))  # Removes 20
print("Queue after removing at index 1:")
myQueue.printQueue()

print("Current size of the queue:", myQueue.size()) 

############################################################
# question 2 b
# Create the queue and add items 1 to 6
q = Que()
for val in [6, 5, 4, 3, 2, 1]:
    q.enqueue(val)

print ('question 2 b :-')
print("Original Queue (Front to Back):")
q.printQueue() # Displays the internal list

# Run the removal method
q.removeEverysec()

print("Queue after removeEverySecond():")
q.printQueue() # Should represent [5, 3, 1] internally based on your insert(0) logic