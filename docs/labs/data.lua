return {
  linear_structures = {
    caption = "Time and Space Complexity Analysis for Linked List (Cormen et al., 2022)",
    -- These MUST match the row keys exactly:
    headers = {"name", "singly", "doubly", "stack"}, 
    rows = {
        { name = "Insert (Front)", singly = "$O(1)$", doubly = "$O(1)$", stack = "$O(1)$" },
        { name = "Insert (End)",   singly = "$O(n)$", doubly = "$O(1)$", stack = "$O(1)$"  },
        { name = "Delete (Head)",  singly = "$O(1)$", doubly = "$O(1)$", stack = "$O(1)$" },
        { name = "Search",         singly = "$O(n)$", doubly = "$O(n)$", stack = "$O(n)$"  },
        { name = "Space",          singly = "$O(n)$", doubly = "$O(n)$", stack = "$O(n)$" }
    }
  },
}