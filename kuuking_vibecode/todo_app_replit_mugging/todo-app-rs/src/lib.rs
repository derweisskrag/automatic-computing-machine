use pyo3::prelude::*;
use std::collections::HashMap;

// ---------------------------------------------------------------------------
// Index-based doubly-linked list (safe Rust, same algorithmic behaviour as
// a pointer-based DLL; avoids unsafe while still exercising the same O(1)
// head/tail push and O(1) node unlink that raw-pointer DLLs provide).
// ---------------------------------------------------------------------------

#[derive(Clone)]
struct Node {
    task: String,
    priority: i64,
    prev: Option<usize>,
    next: Option<usize>,
}

#[pyclass]
pub struct RustDLLPQ {
    nodes: Vec<Option<Node>>,
    free_slots: Vec<usize>,
    head: Option<usize>,
    tail: Option<usize>,
    index: HashMap<String, usize>, // task name → slot
    size: usize,
}

impl RustDLLPQ {
    fn alloc(&mut self, task: String, priority: i64) -> usize {
        let node = Node { task, priority, prev: None, next: None };
        if let Some(slot) = self.free_slots.pop() {
            self.nodes[slot] = Some(node);
            slot
        } else {
            let slot = self.nodes.len();
            self.nodes.push(Some(node));
            slot
        }
    }

    fn free(&mut self, slot: usize) {
        self.nodes[slot] = None;
        self.free_slots.push(slot);
    }

    /// Unlink slot from the DLL; does NOT free or touch `index`.
    fn unlink(&mut self, slot: usize) {
        let (prev, next) = {
            let n = self.nodes[slot].as_ref().unwrap();
            (n.prev, n.next)
        };
        if let Some(p) = prev {
            self.nodes[p].as_mut().unwrap().next = next;
        } else {
            self.head = next;
        }
        if let Some(nx) = next {
            self.nodes[nx].as_mut().unwrap().prev = prev;
        } else {
            self.tail = prev;
        }
        let n = self.nodes[slot].as_mut().unwrap();
        n.prev = None;
        n.next = None;
    }
}

#[pymethods]
impl RustDLLPQ {
    #[new]
    pub fn new() -> Self {
        RustDLLPQ {
            nodes: Vec::new(),
            free_slots: Vec::new(),
            head: None,
            tail: None,
            index: HashMap::new(),
            size: 0,
        }
    }

    /// Insert a new task at the head (front) of the list.
    pub fn push_head(&mut self, task: String, priority: i64) -> bool {
        if self.index.contains_key(&task) {
            return false;
        }
        let slot = self.alloc(task.clone(), priority);
        self.index.insert(task, slot);
        if let Some(old_head) = self.head {
            self.nodes[slot].as_mut().unwrap().next = Some(old_head);
            self.nodes[old_head].as_mut().unwrap().prev = Some(slot);
        } else {
            self.tail = Some(slot);
        }
        self.head = Some(slot);
        self.size += 1;
        true
    }

    /// Insert a new task at the tail (back) of the list.
    pub fn push_tail(&mut self, task: String, priority: i64) -> bool {
        if self.index.contains_key(&task) {
            return false;
        }
        let slot = self.alloc(task.clone(), priority);
        self.index.insert(task, slot);
        if let Some(old_tail) = self.tail {
            self.nodes[slot].as_mut().unwrap().prev = Some(old_tail);
            self.nodes[old_tail].as_mut().unwrap().next = Some(slot);
        } else {
            self.head = Some(slot);
        }
        self.tail = Some(slot);
        self.size += 1;
        true
    }

    /// Remove and return (task, priority) for the node with the highest priority.
    /// O(n) linear scan — same as the Python DLL implementation.
    pub fn pop_max(&mut self) -> Option<(String, i64)> {
        if self.size == 0 {
            return None;
        }
        // Linear scan for max priority
        let mut best = self.head?;
        let mut best_pri = self.nodes[best].as_ref()?.priority;
        let mut cur = self.nodes[best].as_ref()?.next;
        while let Some(slot) = cur {
            let n = self.nodes[slot].as_ref()?;
            if n.priority > best_pri {
                best_pri = n.priority;
                best = slot;
            }
            cur = n.next;
        }
        // Snapshot task name before unlink mutates the node
        let task_name = self.nodes[best].as_ref().unwrap().task.clone();
        self.unlink(best);
        self.index.remove(&task_name);
        self.free(best);
        self.size -= 1;
        Some((task_name, best_pri))
    }

    /// Swap the *priority values* of two tasks in O(1).
    /// This is the key operation heapq cannot perform efficiently.
    pub fn swap_nodes(&mut self, task1: &str, task2: &str) -> bool {
        let slot1 = match self.index.get(task1) { Some(&s) => s, None => return false };
        let slot2 = match self.index.get(task2) { Some(&s) => s, None => return false };
        if slot1 == slot2 { return true; }
        let p1 = self.nodes[slot1].as_ref().unwrap().priority;
        let p2 = self.nodes[slot2].as_ref().unwrap().priority;
        self.nodes[slot1].as_mut().unwrap().priority = p2;
        self.nodes[slot2].as_mut().unwrap().priority = p1;
        true
    }

    /// Peek at (task, priority) of the highest-priority node without removing it.
    pub fn peek(&self) -> Option<(String, i64)> {
        if self.size == 0 {
            return None;
        }
        let mut best = self.head?;
        let mut best_pri = self.nodes[best].as_ref()?.priority;
        let mut cur = self.nodes[best].as_ref()?.next;
        while let Some(slot) = cur {
            let n = self.nodes[slot].as_ref()?;
            if n.priority > best_pri {
                best_pri = n.priority;
                best = slot;
            }
            cur = n.next;
        }
        let n = self.nodes[best].as_ref()?;
        Some((n.task.clone(), n.priority))
    }

    /// Return the whole list as-linked (head → tail order).
    pub fn to_list(&self) -> Vec<(String, i64)> {
        let mut out = Vec::with_capacity(self.size);
        let mut cur = self.head;
        while let Some(slot) = cur {
            if let Some(n) = &self.nodes[slot] {
                out.push((n.task.clone(), n.priority));
                cur = n.next;
            } else {
                break;
            }
        }
        out
    }

    pub fn __len__(&self) -> usize {
        self.size
    }

    pub fn clear(&mut self) {
        self.nodes.clear();
        self.free_slots.clear();
        self.head = None;
        self.tail = None;
        self.index.clear();
        self.size = 0;
    }
}

#[pymodule]
fn todo_app_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<RustDLLPQ>()?;
    Ok(())
}
