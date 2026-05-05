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

#######################################################
# question 2 b
    def splitqueue(self):
        # find the middle point
        mid = self.size() // 2

        # create two new queue objects
        first_half = Que()
        second_half = Que()

        # divide the item using list slicing
        first_half.items = self.items[:mid] # the front half
        second_half.items = self.items[mid:] # the back half

        # return both new queues
        return first_half, second_half


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

###################################################################
# question 2 b testing
# Create and fill the queue
q = Que()
# Adding elements so the list looks like [6, 5, 4, 3, 2, 1]
# Because enqueue(1) goes to index 0, then enqueue(2) pushes it back.
for i in range(6, 0, -1):
    q.enqueue(i)

print("Original Queue:")
q.printQueue() # Output: [1, 2, 3, 4, 5, 6]

# Split the queue
q1, q2 = q.splitqueue()

print("splitQueue():")
q1.printQueue() # Output: [1, 2, 3]
q2.printQueue() # Output: [4, 5, 6]