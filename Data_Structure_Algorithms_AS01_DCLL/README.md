# **DOUBLY CIRCULAR LINKED LIST (DCLL) Implementation**



#### 

### **Project Overview**

This project implements a robust Doubly Circular Linked List data structure. Unlike a standard linked list, a DCLL allows for bidirectional traversal, and the tail node points back to the head node (and vice versa), creating a continuous loop. This implementation includes a fixed capacity limit and built-in integrity simulations to ensure data consistency during operations.



### **Key Features**

* Fixed Capacity: Includes a limit attribute to prevent memory overflow and manage list size effectively.



* Bidirectional Pointers: Each node contains a next and prev pointer for efficient forward and backward navigation.



* Circular Logic: The list maintains a perfect circle where head.prev always points to the last element, and the last element's next points back to the head.



* Sorting Integrity: Includes a dedicated simulation suite to verify that the list remains logically sound after insertions, deletions, and reversals.





### **Operational Included**

* add(item): Inserts a new element at the end of the list, provided the limit has not been reached.



* delete(item): Locates and removes a specific value, re-linking the surrounding nodes to maintain the circular structure.



* search(item): Traverses the list to find a specific value, returning its presence without modifying the structure.



* display(): Prints the current state of the list in a readable format (e.g., 10 <-> 20 <-> 30).



* reverse(): Flips the direction of all next and prev pointers, effectively reversing the list while maintaining its circular nature.





### **Technical Specifications**

Language: Python 3.x



Complexity:



* Insertion: O(1) (due to circular tail access)



* Deletion/Search: O(n)



* Space Complexity: O(n)

