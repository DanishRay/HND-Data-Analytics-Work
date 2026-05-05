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