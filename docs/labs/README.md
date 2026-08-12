---
geometry:
  - a4paper
  - left=3cm
  - right=2cm
  - top=2.5cm
  - bottom=2.5cm
linestretch: 1.5
header-includes:
  - \usepackage{float}
  - \usepackage{titlesec}
  - |
    \titleformat{\section}{\fontsize{14pt}{17pt}\selectfont\bfseries\uppercase}{\thesection.}{1em}{}
    \titlespacing*{\section}{0pt}{12pt}{20pt}
    \titleformat{\subsection}{\fontsize{12pt}{15pt}\selectfont\bfseries}{\thesubsection.}{1em}{}
    \titlespacing*{\subsection}{0pt}{12pt}{12pt}
    \titleformat{\subsubsection}{\fontsize{12pt}{15pt}\selectfont\bfseries}{\thesubsubsection.}{1em}{}
    \titlespacing*{\subsubsection}{0pt}{12pt}{12pt}
  - \usepackage{graphicx}
  - \usepackage{times}

  - \usepackage{inconsolata} 
  - \usepackage{soul}
  - \DeclareTextFontCommand{\texttt}{\ttfamily\small}

  - \usepackage[singlelinecheck=false]{caption}
  - |
    \captionsetup[table]{position=above, justification=raggedright}
    \captionsetup[figure]{position=below, justification=raggedright}


---

# INTRODUCTION { - }

For the homework, I will re-use my own Kuuking DSA library that uses Rust and Python. I will try to create mini-version (demo) of Task Scheduler. It involves my own library (see Appendix of the current document) written in Python and the Rust module (via Maturin).


## 1. Todo Scheduler

The idea is to try out my own PriorityQueue written in both Python and Rust. Yes, you can try

```py
from dsa_kuuking.queues.priority_queue.implementation.priority_queue import PriorityQueue
start = time.time()
r = PriorityQueue()
for i in range(10000):
    r.enqueue(f"Task {i}", i)
print(f"(Python) 10k enqueues: {time.time() - start:.4f}s")
```

It is not problem, but we are exploring the Rust function written by me

```rs
#[pymethods]
impl PriorityQueue {
    #[new]
    fn new() -> Self {
        PriorityQueue { queue: Mutex::new(Vec::new()) }
    }

    fn push(&self, py: Python, priority: i32, item: PyObject) {
        // ALLOW-THREADS: Releasing the GIL so other threads can run Python code
        // while Rust is busy sorting the Vec.
        py.allow_threads(move || {
            let mut data = self.queue.lock().unwrap();
            data.push((priority, item));
            data.sort_unstable_by(|a, b| b.0.cmp(&a.0));
        });
    }

    fn pop(&self, py: Python) -> Option<PyObject> {
        py.allow_threads(move || {
            let mut data = self.queue.lock().unwrap();
            data.pop().map(|(_prio, item)| item)
        })
    }
}
```

### Task Class

The task can be added using the class

```py
class Task:
    """
    A task, a todo that has a name and priority. It is used for the 'Queue'.

    Example:
    >>> watch_tv = Task(3, "Watch TV")
    >>> print(watch_tv)
    """
    def __init__(self, priority, name):
        self.name = name
        self.priority = priority

    def __str__(self):
        return f"Task(name={self.name}, priority={self.priority})"
```

For example,

```py
make_tea = Task(2, "Make Tea")
pq.add_task(make_tea) # Adds the task
```

Since we did not implement it, but it can re-use some HTTPS API Service to send notification or execute the tasks by itself. What does it mean? It means automation. People can use API to add new tasks for the system and servers run those concurrently. However, we implement it in the simple case: just trying out the function. 

### Queue 

This is the queue (priority one) for our tasks. Technically, we can omit the class entirely, but since it was incomplete implementation in Rust or they want to add more features to it in Python, then they wrap it in Python class.

```py
class Queue:
    def __init__(self):
        self.tasks = PriorityQueue()
        # TODO: Temporary fix
        self.size = 0

    def add_task(self, task):
        self.tasks.push(task.priority, task.name)
        self.size += 1

    def get_next_task(self):
        if self.size > 0:
            self.size -= 1
            return self.tasks.pop()
        else:
            return None
```

You can try running

```py
start = time.time()
pq = PriorityQueue ()
for i in range(10000):
    pq.push(i, f"Task {i}")
print(f"(Rust) 10k enqueues: {time.time() - start:.4f}s")
```

and then you can try

```py
pq = Queue()
start = time.time()
for i in range(10000):
    pq.add_task(Task(i, f"Task {i}"))
print(f"(Rust) 10k enqueues: {time.time() - start:.4f}s")
```

For example, on my machine, it gave

```
>>> py main.py
(Rust) 10k enqueues: 0.6460s
```

As you can see, it worked the same. 

### Example

```py
if __name__ == "__main__":
    task_eat_dinner = Task(2, "Eat Dinner")
    task_do_homework = Task(1, "Do Homework")

    task_watch_tv = Task(3, "Watch PrimeTimeAgen - Rust")
    pq = Queue()
    pq.add_task(task_eat_dinner)
    pq.add_task(task_do_homework)
    pq.add_task(task_watch_tv)

    print("Tasks in priority order:")
    while True:
        next_task = pq.get_next_task()
        if next_task is None:
            break
        print(next_task)
```

## CONCLUSION

In this homework, we have implemented a simple Task Scheduler using a Priority Queue. We have demonstrated how to use both Python and Rust implementations of the Priority Queue, and how to integrate them into a simple task management system. The Rust implementation provides better performance for large numbers of tasks, while the Python implementation offers ease of use and flexibility. This exercise has shown the benefits of using Rust for performance-critical components while maintaining the simplicity of Python for higher-level logic.

# APPENDICES

## Appendix 1. Digital repository (GitHub)

The complete implementation of the Data Structures and Algorithms discussed in this thesis, including the Python baseline and the Rust/Wasm modules, is available in the following GitHub repository:

- PyPI: https://pypi.org/project/dsa-kuuking/
- Test PyPI: https://test.pypi.org/project/dsa-kuuking/
- GitHub: https://github.com/derweisskrag/DSA
- Commit Hash: a0b2e8c
- License: MIT
