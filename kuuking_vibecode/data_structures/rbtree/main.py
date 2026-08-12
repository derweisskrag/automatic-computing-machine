"""
This module contains the Red-black tree implementation
"""

"""
INSERT

    Denote Nodes:
        New node - K
        Parent - P ('parent')
        Uncle - U (Defined as 'parent.parent.left')
        Sibling - S ('parent.left' or 'parent.right' depending on K's location)
        Grandparent - G ('parent.parent')

    case 1: Tree is empty: create new root and colour it to be black.
    case 2: If K's parent is Black - Ok.
    case 3: K's P is RED: property 4 is violated: new node and parent are RED
    the G must be BLACK node because the tree before insertion must be a
    valid red-black tree. To resolve this case, we need to check if new node uncle is
    RED or BLACK.
        case 3.1: Uncle is RED too (P=RED, U=RED). We have to flip the colours of
        P, G and U. That means, P becomes Black, U becomes Black and G becomes RED.
        Conclusion: Re-colour.
        Edge Case at 3.1: If G is a root, we don't colour it RED (root is never RED).
    
        case 3.2: P is RED and U is either BLACK or None (NIL). This is more complicated
        than the previous case. If the Uncle (U) is BLACK, we need single double tree
        rotations depending upon whether K is a left or right child of P.
            case 3.2.1: P is the right child of G and K is right child of P:
            Example plot:
                2 (Black) = Root                     2 (Black)
              /  \\                                 /   \\
        1 (Black) 4 (Black) = G   --->       1 (Black)  5 (Red) = Make Black
                /  \\                                   / \\
          3 (Black) 5 (Red) = P            Make Red:  4 (Black) 6 (Red)
          This is U  \\                              /
                 /    6 (Red) This is K         None
        S: sibling is None
    
            First, we perform the left-rotation at G that makes G to be S of K. Next, we change
            the colour of S to RED and P's to BLACK.
            Case 3.2.2: P is right child of G and K is the left child of P. In this case, we
            have to right-rotation at P. This reduces it to the case 3.2.1. We next use the rules
            given in 3.2.1 to fix the tree.
            Case 3.2.3: P is the left child of G and K is the left child of P. This is the mirror of
            the case 3.2.1 (solution is symmetric to 3.2.1 - Apply Right-rotation and re-colour).
            Case 3.2.4: P is the left child of G and K is the right child of P. This is mirror of the
            case 3.2.2. Therefore, we have to apply left-rotation, and then right-rotation (3.2.2).
                
               
REMOVE NODE 
                
    x - node to delete
    S - Sibling
    G - Grandparent
    P - Parent
    
    The first step is to follow BST deletion process. Then we fix the balance.
    
    Case 1: x is a RED node. In this case, we simply delete x, because the removal
    of a red nodes doesn't violate the rules.
    Case 2: x has a RED child. We replace x by its child and change the colour of
    the child to RED. This way, we retain the property 5 (Every path from root to leaf
    must be equal for BLACK Nodes).
    Case 3: x is a BLACK node. Deleting a BLACK node violates the aforementioned rule.
    So, we add an extra BLACK node to the deleted node and call it a "double black" node.
    Now we need to convert this "double black node" into the BLACK node. For this, we consider
    the following 8 cases in total (4 are mirror).
    
    Case 3.1: x's S is RED. In this case, we switch the colours of S and 'x.parent', and then
    perform the left rotation on 'x.parent'. This reduces the case 3.1 to case 3.2, 3.3 or 3.4
    
    Case 3.2: x's S is BLACK, and both children of S are BLACK. The color of x's parent can
    be BLACK or RED. We switch the colour of S to RED. If the colour of x's parent is RED, we switch
    its colour to BLACK and this becomes terminal case. Otherwise, we make x's parent a new x and repeat
    the process from case 3.1.
    
    Case 3.3: x's S is BLACK, and S's left child is RED, and the right child of S is BLACK. We can
    switch the colours of S and its left child 'S.left' and then perform right rotation on S without
    violating any of the red-black properties. This transforms the tree into 3.4 case.
    
    Case 3.4: x's S is BLACK, and S's right child is RED. This is the terminal case. We change the colour
    of S's right child to BLACK, 'x.parent' colour to BLACK, x' S to RED and then perform the left rotation on the x's
    parent node. This way, we remove the extra black node on x.
    X is the node to removed, but target was x.parent. We just copy value it into parent.
"""
import random

from typing import Optional, Tuple, TypeVar, Union, override

T = TypeVar("T")
E = TypeVar("E")

from enum import Enum


class Color(Enum):
    RED = "RED"
    BLACK = "BLACK"


from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Union

class NIL:
    def __init__(self) -> None:
        self.key = None
        self.value = None

        # pointers
        self.left = self
        self.right = self
        self.parent = None

        # color
        self.color = Color.BLACK

    def __str__(self) -> str:
        return f"NIL"


class Node[T]:
    def __init__(self, key: T, value: T, color: Optional[Color] = Color.RED) -> None:
        # assign values
        self.key = key
        self.value = value

        # check for the values
        assert key is not None, f"Key cannot be None: {key}"
        assert value is not None, f"Value cannot be None: {value}"

        # assign pointers
        self.left = NIL()
        self.left.parent = self
        self.right = NIL()
        self.right.parent = self
        self.parent = None  # parent is None, not NIL

        # colour is always RED
        self.color = color

    def __str__(self) -> str:
        return f"Node(key={self.key}, value={self.value}, color={self.color})"




class RBTreeInterface[T](ABC):
    @abstractmethod
    def add(self, key: T, value: T) -> None: ...

    @abstractmethod
    def remove(self, key: T) -> Optional[Node[T]]: ...

    @abstractmethod
    def swap(self, u: Node[T], v: Node[T]) -> None: ...

    @abstractmethod
    def is_empty(self) -> bool: ...

    @abstractmethod
    def get_node_or_mock(self, node: Node[T]) -> Optional[Union[NIL, Node[T]]]: ...

    @abstractmethod
    def find_by_key(self, key: T) -> Optional[Node[T]]: ...

    @abstractmethod
    def count_children(self, node: Node[T]) -> int: ...

    @staticmethod
    @abstractmethod
    def node_exists(node: Union[NIL, Node[T]]) -> bool: ...

    @staticmethod
    @abstractmethod
    def is_leaf(node: Union[Node[T], NIL]) -> bool: ...

    @abstractmethod
    def predecessor(self, node: Union[NIL, Node[T]]) -> Node[T]: ...

    @abstractmethod
    def successor(self, node: Union[NIL, Node[T]]) -> Node[T]: ...

    @abstractmethod
    def in_order_traverse(self, node: Node[T]) -> None: ...

    @abstractmethod
    def pre_order_traverse(self, node: Node[T]) -> None: ...

    @abstractmethod
    def post_order_traverse(self, node: Node[T]) -> None: ...



class ResultType[T, E]:
    def __init__(self, value: Optional[T] = None, error: Optional[E] = None) -> None:
        self.value = value
        self.error = error

    def is_ok(self):
        return self.error is None

    def is_err(self):
        return self.error is not None

    def unwrap(self) -> T:
        if self.is_err():
            raise ValueError(f"Called unwrap on an error result: {self.error}")
        return self.value

    def unwrap_err(self) -> E:
        if self.is_ok():
            raise ValueError(f"Called unwrap_err on an ok result: {self.value}")
        return self.error


class RBTree[T](RBTreeInterface):
    def __init__(self, *args: Optional[Tuple[T]]) -> None:
        self._root = NIL()
        self.NIL_LEAF = self._root
        self.size = 0

        if len(args) >= 1:
            for key, value in args:
                self.add(key, value)

    @override
    def add(self, key: T, value: T) -> None:
        new_node = Node(key, value)
        parent = None
        current = self._root

        while not isinstance(current, NIL):
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent
        if parent is None:
            self._root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self.size += 1
        self._fix_insert(new_node)

    def _insert(self, node: Node[T]) -> Node[T]:
        current = self._root
        parent = None
        while not isinstance(current, NIL):
            parent = current
            if node.key < current.key:
                current = current.left
            else:
                current = current.right

        node.parent = parent
        if parent is None:
            self._root = node
        elif node.key < parent.key:
            parent.left = node
        else:
            parent.right = node

        return node

    def remove_copilot(self, key: T) -> Optional[Node[T]]:
        return self.remove(key)

    @override
    def remove(self, key: T) -> Optional[Node[T]]:
        node_to_delete = self.find_by_key(key)
        if node_to_delete is None:
            return None

        removed_node = node_to_delete
        removed_color = removed_node.color
        if isinstance(node_to_delete.left, NIL):
            replacement = node_to_delete.right
            self.transplant(node_to_delete, node_to_delete.right)
        elif isinstance(node_to_delete.right, NIL):
            replacement = node_to_delete.left
            self.transplant(node_to_delete, node_to_delete.left)
        else:
            successor = self._min(node_to_delete.right)
            removed_color = successor.color
            replacement = successor.right
            if successor.parent == node_to_delete:
                replacement.parent = successor
            else:
                self.transplant(successor, successor.right)
                successor.right = node_to_delete.right
                successor.right.parent = successor

            self.transplant(node_to_delete, successor)
            successor.left = node_to_delete.left
            successor.left.parent = successor
            successor.color = node_to_delete.color

        if removed_color == Color.BLACK:
            self._fix_remove(replacement)

        self.size = max(0, self.size - 1)
        if isinstance(self._root, NIL) and self._root is not self.NIL_LEAF:
            self._root = self.NIL_LEAF
        return removed_node

    def remove_node_alek_os(self, key: T) -> Optional[Node[T]]:
        return self.remove(key)

    def _fix_insert(self, node: Node[T]) -> None:
        while node.parent is not None and node.parent.color == Color.RED:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == Color.RED:
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == Color.RED:
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._left_rotate(node.parent.parent)

        self._root.color = Color.BLACK

    def _fix_remove(self, node: Node[T]) -> None:
        while node != self._root and node.color == Color.BLACK:
            if node == node.parent.left:
                sibling = node.parent.right
                if sibling.color == Color.RED:
                    sibling.color = Color.BLACK
                    node.parent.color = Color.RED
                    self._left_rotate(node.parent)
                    sibling = node.parent.right

                if sibling.left.color == Color.BLACK and sibling.right.color == Color.BLACK:
                    sibling.color = Color.RED
                    node = node.parent
                else:
                    if sibling.right.color == Color.BLACK:
                        sibling.left.color = Color.BLACK
                        sibling.color = Color.RED
                        self._right_rotate(sibling)
                        sibling = node.parent.right

                    sibling.color = node.parent.color
                    node.parent.color = Color.BLACK
                    sibling.right.color = Color.BLACK
                    self._left_rotate(node.parent)
                    node = self._root
            else:
                sibling = node.parent.left
                if sibling.color == Color.RED:
                    sibling.color = Color.BLACK
                    node.parent.color = Color.RED
                    self._right_rotate(node.parent)
                    sibling = node.parent.left

                if sibling.left.color == Color.BLACK and sibling.right.color == Color.BLACK:
                    sibling.color = Color.RED
                    node = node.parent
                else:
                    if sibling.left.color == Color.BLACK:
                        sibling.right.color = Color.BLACK
                        sibling.color = Color.RED
                        self._left_rotate(sibling)
                        sibling = node.parent.left

                    sibling.color = node.parent.color
                    node.parent.color = Color.BLACK
                    sibling.left.color = Color.BLACK
                    self._right_rotate(node.parent)
                    node = self._root

        node.color = Color.BLACK

    def _left_rotate(self, node: Node[T]) -> None:
        right_child = node.right
        node.right = right_child.left
        right_child.left.parent = node

        right_child.parent = node.parent
        if node.parent is None:
            self._root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    def _right_rotate(self, node: Node[T]) -> None:
        left_child = node.left
        node.left = left_child.right
        left_child.right.parent = node

        left_child.parent = node.parent
        if node.parent is None:
            self._root = left_child
        elif node == node.parent.left:
            node.parent.left = left_child
        else:
            node.parent.right = left_child

        left_child.right = node
        node.parent = left_child

    def transplant(self, u: Node[T], v: Union[NIL, Node[T]]) -> None:
        if u.parent is None:
            self._root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        v.parent = u.parent

    @staticmethod
    @override
    def node_exists(node: Union[Node[T], NIL]) -> bool:
        return not isinstance(node, NIL)

    @override
    def count_children(self, node: Node[T]) -> int:
        return 2 if self.node_exists(node.left) and self.node_exists(node.right) else \
            1 if self.node_exists(node.left) or self.node_exists(node.right) else 0

    @override
    def get_node_or_mock(self, node: Node[T]) -> Optional[Union[NIL, Node[T]]]:
        return node.left if self.node_exists(node.left) else node.right

    @staticmethod
    def _min(node: Union[NIL, Node[T]]) -> Node[T]:
        minimum = node
        while not isinstance(node, NIL):
            minimum = node
            node = node.left

        return minimum

    @staticmethod
    def _max(node: Union[NIL, Node[T]]) -> Node[T]:
        maximum = node
        while not isinstance(node, NIL):
            maximum = node
            node = node.right

        return maximum

    @override
    def predecessor(self, node: Union[NIL, Node[T]]) -> Optional[Node[T]]:
        if isinstance(node, NIL):
            return None
        if not isinstance(node.left, NIL):
            return self._max(node.left)

        parent = node.parent
        while parent is not None and node == parent.left:
            node = parent
            parent = parent.parent

        return parent

    @override
    def successor(self, node: Union[NIL, Node[T]]) -> Optional[Node[T]]:
        if isinstance(node, NIL):
            return None
        if not isinstance(node.right, NIL):
            return self._min(node.right)

        parent = node.parent
        while parent is not None and node == parent.right:
            node = parent
            parent = parent.parent

        return parent

    @override
    def in_order_traverse(self, node: Union[NIL, Node[T]]) -> None:
        if not isinstance(node, NIL):
            self.in_order_traverse(node.left)
            print(f"Node (key - value - color): {node.key} - {node.value} - {node.color}")
            self.in_order_traverse(node.right)

    @override
    def pre_order_traverse(self, node: Union[NIL, Node[T]]) -> None:
        if not isinstance(node, NIL):
            print(f"Node (key - value - color): {node.key} - {node.value} - {node.color}")
            self.pre_order_traverse(node.left)
            self.pre_order_traverse(node.right)

    @override
    def post_order_traverse(self, node: Union[NIL, Node[T]]) -> None:
        if not isinstance(node, NIL):
            self.post_order_traverse(node.left)
            self.post_order_traverse(node.right)
            print(f"Node (key - value - color): {node.key} - {node.value} - {node.color}")

    @override
    def swap(self, u: Node[T], v: Node[T]) -> None:
        u.key, v.key = v.key, u.key
        u.value, v.value = v.value, u.value
        u.color, v.color = v.color, u.color

    @override
    def find_by_key(self, key: T) -> Optional[Node[T]]:
        current = self._root
        while not isinstance(current, NIL):
            if key == current.key:
                return current
            if key < current.key:
                current = current.left
            else:
                current = current.right
        return None

    @staticmethod
    def find_uncle(node: Node[T]) -> Union[NIL, Node[T]]:
        if not (node.parent and node.parent.parent):
            raise Exception("No parent and grandparent exist for this node!")

        if node.parent == node.parent.parent.left:
            return node.parent.parent.right

        return node.parent.parent.left

    def find_sibling(self, node: Node[T]) -> Union[NIL, Node[T]]:
        if node.parent is None:
            return NIL()
        if node == node.parent.left:
            return node.parent.right
        return node.parent.left

    def remove_node(self, key: T) -> Optional[Node[T]]:
        return self.remove(key)

    def remove_rb(self, key: T) -> Optional[Node[T]]:
        return self.remove(key)

    @property
    def root(self) -> Node[T]:
        match self.get_root():
            case result if result.is_ok():
                return result.unwrap()
            case error if result.is_error():
                raise Exception(error.unwrap_err())
            case _:
                raise Exception("Other error")

    def get_root(self) -> ResultType[Node[T], str]:
        """Retrieves the root"""
        if self._root is None:
            return ResultType(error="The root doesn't exist")
        return ResultType(value=self._root)

    @override
    def is_empty(self) -> bool:
        return self._root is None or isinstance(self._root, NIL)

    @staticmethod
    @override
    def is_leaf(node: Union[Node[T], NIL]) -> bool:
        # has no children
        return isinstance(node.left, NIL) and isinstance(node.right, NIL)

    def verify_properties(self) -> bool:
        """Verifies Red-Black Tree invariants: Root color, Red-Red checks, and Black Height parity."""
        if isinstance(self._root, NIL):
            return True

        # Property 2: Root must be BLACK
        if self._root.color != Color.BLACK:
            print("Violation: Root is not BLACK")
            return False

        def _check_node(node: Node[T]) -> tuple[bool, int]:
            if isinstance(node, NIL):
                return True, 1  # NIL leaves count as 1 black node

            # Property 4: No RED node has a RED child
            if node.color == Color.RED:
                if node.left.color == Color.RED or node.right.color == Color.RED:
                    print(f"Violation: Red-Red hazard at key {node.key}")
                    return False, 0

            left_ok, left_black_height = _check_node(node.left)
            right_ok, right_black_height = _check_node(node.right)

            if not left_ok or not right_ok:
                return False, 0

            # Property 5: Equal black height across all paths
            if left_black_height != right_black_height:
                print(f"Violation: Black height mismatch at key {node.key} (left={left_black_height}, right={right_black_height})")
                return False, 0

            current_black = 1 if node.color == Color.BLACK else 0
            return True, left_black_height + current_black

        ok, _ = _check_node(self._root)
        return ok


# def main():
#     rb = RBTree[int]()
#     rb.add(key=1, value=15)
#     rb.add(key=2, value=13)
#     rb.add(key=3, value=16)
#     rb.add(key=4, value=19)
#     rb.add(key=5, value=20)
#     rb.add(key=6, value=23)
#     rb.add(key=7, value=29)
#     rb.add(key=8, value=31)
#     rb.add(key=9, value=32)
#     rb.add(key=10, value=33)
#     rb.add(key=11, value=51)
#     rb.add(key=12, value=39)
#     print("BEFORE REMOVAL")
#     rb.in_order_traverse(rb.root)

#     print()
#     print("AFTER REMOVAL")
#     rb.remove(10)
#     rb.in_order_traverse(rb.root)


# if __name__ == "__main__":
#     main()


def run_rb_tree_stress_test():
    rb = RBTree[int]()
    
    # Standard 1-12 dataset
    initial_keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    for k in initial_keys:
        rb.add(key=k, value=k * 10)

    print("=== INITIAL TREE (IN-ORDER WITH PARENTS) ===")
    rb.in_order_traverse(rb.root)
    print("\nRoot key:", rb.root.key if rb.root else "NONE")


    # TEST 0: Verify Tree
    print("=== VERIFY TREE ===")
    print(rb.verify_properties())

    # TEST 1: Delete a key (Leaf / Black Node Deletion)
    print("\n--- TEST 1: Deleting Key 8 ---")
    rb.remove(8)
    rb.in_order_traverse(rb.root)

    # TEST 2: Delete Root Node
    current_root_key = rb.root.key
    print(f"\n--- TEST 2: Deleting Current Root (Key {current_root_key}) ---")
    rb.remove(current_root_key)
    rb.in_order_traverse(rb.root)
    print("New Root key:", rb.root.key if rb.root else "NONE")

    # TEST 3: Drain Test (Delete remaining nodes one by one)
    print("\n--- TEST 3: Sequential Drain Test ---")
    remaining_keys = [k for k in initial_keys if k != 8 and k != current_root_key]
    random.shuffle(remaining_keys)
    
    for key in remaining_keys:
        print(f"Removing key {key}...")
        rb.remove(key)
        
    print("\n=== FINAL TREE (SHOULD BE EMPTY OR ONLY NIL) ===")
    if rb.root is None or isinstance(rb.root, NIL):
        print("Success! Tree successfully drained to empty NIL root.")
    else:
        rb.in_order_traverse(rb.root)

if __name__ == "__main__":
    run_rb_tree_stress_test()
