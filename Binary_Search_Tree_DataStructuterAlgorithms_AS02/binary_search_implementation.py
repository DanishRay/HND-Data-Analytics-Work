## Binaary Search Tree implementation in Python

## Defining the node and the tree structure
class Node:
    def __init__(self, key):
        self.key = key
        self.count = 1  
        self.left = None
        self.right = None
## *Handling duplicates keys, the NODE class should include a COUNT attribute to keep track of the number of occurrences of each key.


class BinarySearchTree:
#----------------------------------------------#
    ## Implementing Add(Item)
    def add(self, root, key):
        # Standard BST insertion logic
        if root is None:
            return Node(key)
        
        # Handle duplicates 
        if key == root.key:
            root.count += 1
            return root
        
        # Recursive insertion
        if key < root.key:
            root.left = self.add(root.left, key)
        else:
            root.right = self.add(root.right, key)
        return root
    ## The ADD function is modified to handle duplicate keys
    ## If the key already exists, it increment the count instead of creating a new node.
#----------------------------------------------#
    ## Implementing CheckDuplicate(item)
    def check_duplicate(self, root, key):
        if root is None:
            return False
        if root.key == key:
            return root.count > 1  # Returns True if count > 1 
        if key < root.key:
            return self.check_duplicate(root.left, key)
        return self.check_duplicate(root.right, key)
    ## This operation checks if an item is duplicated in the tree and returns a Boolean result
#----------------------------------------------#
    ## Implementing DeleteMax() and DeleteMin()
    def delete_min(self, root):
        if root is None: return None, None
        # Move to the leftmost node 
        if root.left is None:
            return root.right, root.key
        new_left, deleted_item = self.delete_min(root.left)
        root.left = new_left
        return root, deleted_item

    def delete_max(self, root):
        if root is None: return None, None
        # Move to the rightmost node 
        if root.right is None:
            return root.left, root.key
        new_right, deleted_item = self.delete_max(root.right)
        root.right = new_right
        return root, deleted_item
    ## These operations must delete the extreme values and return the deleted item
#----------------------------------------------#
    ## Implementing SearchByRange(range1, range2)
    def search_by_range(self, root, r1, r2, result):
        if root is None:
            return
        # If root's key is greater than range1, check left subtree
        if r1 < root.key:
            self.search_by_range(root.left, r1, r2, result)
        # If root's key is within range, add it
        if r1 <= root.key <= r2:
            for _ in range(root.count):
                result.append(root.key)
        # If root's key is less than range2, check right subtree 
        if r2 > root.key:
            self.search_by_range(root.right, r1, r2, result)
    ## This operation returns all items within the givne minimum(range1) and maximum (range2) range.
#----------------------------------------------#
    ## Implementing Height() and ChekcBalanceTree()
    def get_height(self, root):
        if root is None:
            return 0  # Height of empty tree is 0 
        return 1 + max(self.get_height(root.left), self.get_height(root.right))

    def check_balance_tree(self, root):
        if root is None:
            return True  # Empty tree is balanced 
        
        lh = self.get_height(root.left)
        rh = self.get_height(root.right)
        
        # Balance condition
        if abs(lh - rh) <= 1 and self.check_balance_tree(root.left) and self.check_balance_tree(root.right):
            return True
        return False
    ## The HEIGH operation returns the tree height
    ## The CHECKBALANCETREE operation returns TRUE if the height difference between left and right subtrees is no more than one for every node

#---------------------------------------------------------------#
## Binary Search Tree Test Cases

# Initialize the Tree and the root
bst = BinarySearchTree()
root = None
print("--- Starting BST Modified Testing ---")
## Before running tests
## Iniitialize the BINARYSEARCHTREE and ROOT variable to track the state of the tree throughout the operations

## Tesing Add(item)
print("\n[1] Testing Add(item)")
# 1. Add to empty tree
root = bst.add(root, 50)
# 2. Add multiple no duplicates
root = bst.add(root, 30)
root = bst.add(root, 70)
# 3. Add duplicate items
root = bst.add(root, 30) 
# 4. Verify structure/count
print(f"Root: {root.key}, Left: {root.left.key} (Count: {root.left.count}), Right: {root.right.key}")
## This test case section verifies the tree handles empty states, unique item, and the specific requirement for duplicate handling using the COUNT attribute

## Testing CheckDuplicate(item)
print("\n[2] Testing CheckDuplicate(item)")
# 1. Check item with count > 1
print(f"Is 30 duplicated? {bst.check_duplicate(root, 30)}") # Expected: True
# 2. Check item with count == 1
print(f"Is 50 duplicated? {bst.check_duplicate(root, 50)}") # Expected: False
# 3. Check non-existent item
print(f"Is 99 duplicated? {bst.check_duplicate(root, 99)}") # Expected: False
## This test case checks the logic that returns TRUE only if item's COUNT is greater than 1

## Testing DeleteMin() and DeleteMax()
print("\n[3 & 4] Testing DeleteMax() and DeleteMin()")
# Delete Max
root, max_val = bst.delete_max(root)
print(f"Deleted Max: {max_val}") # Expected: 70
# Delete Min
root, min_val = bst.delete_min(root)
print(f"Deleted Min: {min_val}") # Expected: 30 (Note: count was 2, now node is gone)
## This test case verifies that the extreme values are removed and returned while maintaining the tree structure

## Testing SearchByRange(range1, range2)
print("\n[5] Testing SearchByRange(20, 60)")
# Re-adding items for a better range test
root = bst.add(root, 20)
root = bst.add(root, 40)
root = bst.add(root, 60)

results = []
bst.search_by_range(root, 25, 55, results)
print(f"Items in range 25-55: {results}") # Expected: [40, 50]
## This test case returns all items within a specified inclusive range

## Testing Height() and CheckBalanceTree()
print("\n[6 & 7] Testing Height() and CheckBalanceTree()")
# 1. Check height
print(f"Current Tree Height: {bst.get_height(root)}") 
# 2. Check balance
print(f"Is Tree Balanced? {bst.check_balance_tree(root)}")

# 3. Create unbalanced state (Add items to one side)
root = bst.add(root, 10)
root = bst.add(root, 5)
print(f"Balanced after adding 10 and 5? {bst.check_balance_tree(root)}")
## This test case is final structural checks to ensure the tree calculates depth and balance correctly accord`ing to the height difference rule.