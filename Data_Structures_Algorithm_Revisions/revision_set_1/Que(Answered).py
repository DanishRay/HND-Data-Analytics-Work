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

#############################################################################
    # question 2 b
    def rotatequeue(self, k):
        # get the current length of the queue
        length = self.size()

        # avoid division by zero if queue is empty
        if length == 0:
            return
        
        # calculate effective rotations (handles k > length)
        k = k % length

        # rotate -> take from front, put in rear k times
        for _ in range(k):
            item = self.dequeue()
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

#############################################################################
# question 2 b testing
# Setup the Queue
q = Que()
for i in [5, 4, 3, 2, 1]: # Enqueueing so front is 1, rear is 5
    q.enqueue(i)

print("Queue:", end=" ")
q.printQueue() # Output: [5, 4, 3, 2, 1] - index 0 is rear, end is front

# Rotate by 2
q.rotatequeue(2)

print("rotateQueue(2):", end=" ")
q.printQueue() # Output: [2, 1, 5, 4, 3]