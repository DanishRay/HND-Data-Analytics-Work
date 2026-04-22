# **Binary Search Tree Implementation Python**

This repository contains my assignment work and my report notes on a Python implementation of Binary Search Tree (BST) with handling for duplicate values and tree balance verification

**\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**



### **Features**

1. **Duplicate Management**
* **Occurrence Counting:** Each node contains a count attribute to track how many times a key is added, rather than creating new nodes for duplicate values.



* **Duplicate Checking:** A dedicated function returns True only if a specific key exists in the tree more than once.



**2. Standard BST Operations**

* **Add:** Inserts a new item or increments the count of an existing item.



* **Search by Range:** Finds and returns a list of all items located between two specific values (inclusive).



* **Delete Min/Max:** Removes the smallest or largest value from the tree and returns the deleted value.



**3. Structural Analysis**

* **Height Calculation:** Returns the total height of the tree.



* **Balance Verification:** Checks if the tree is balanced. A tree is considered balanced if the height difference between the left and right subtrees of every node is no more than one.



**\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**



### **Class Structure**

**Node Class**

* **key:** The data value stored in the node.



* **count:** Number of times the key appears.



* **left:** Reference to the left child node.



* **right:** Reference to the right child node.



**BinarySearchTree Class**

Contains methods for adding nodes, deleting extremes, searching ranges, and measuring tree dimensions.



**\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**



### **Testing**

The script includes automated test cases to verify the following

* Adding items to empty and populated trees.



* Handling duplicate keys via the counter.



* Removing the minimum and maximum elements.



* Filtering items within a numerical range.



* Confirming tree balance after multiple insertions.

