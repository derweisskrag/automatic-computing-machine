from src.kuuking_console.pages.styles import burmese_print

def render_rbtree_dashboard(task_tree):
    burmese_print("TREE", "Inspecting RB-TREE Priority Index (Sorted)... 🌲")
    
    # In-order traversal gives perfectly sorted output!
    sorted_tasks = task_tree.in_order_traverse(task_tree.root) 

    if not sorted_tasks:
        burmese_print("scowls", "\tTree index is currently empty.")
        return

    for node in sorted_tasks:
        burmese_print("found", f"\t [Priority {node.key}]: {node.value}")