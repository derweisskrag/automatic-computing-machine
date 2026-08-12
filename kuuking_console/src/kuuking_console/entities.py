from datetime import datetime
from dataclasses import dataclass

class Action: 
    pass

@dataclass
class AddTodoAction(Action):
    description: str
    due_date: datetime

@dataclass
class AddTaskAction(Action):
    description: str
    priority: int

# So this one is for processing the next task in the queue, which is basically just popping the head node of the queue and logging it as executed.
@dataclass
class ProcessNextAction(Action):
    pass

@dataclass
class ProcessNextTaskAction(Action):
    priority: int

# Look at this:
# This one for cases when you want to change the priority of an existing task in the queue, which is a bit more complex because we need to find the task, remove it, and re-enqueue it with the new priority.
# For example, I know that my sleep is the highest priority at the end of the day
# but it is lowest priority in the morning, so I can change it throughout the day as needed without having to remove and re-add it manually. This is where the flexibility of our priority queue shines, allowing dynamic updates to task priorities on the fly.
@dataclass
class ChangePriorityAction(Action):
    task_title: str
    new_priority: int


@dataclass
class ViewAllTasksAction(Action):
    pass


class Todo:
    def __init__(self, description: str, due_date: datetime):
        self.description = description
        self.due_date = due_date

    def __str__(self):
        return f"{self.description} (Due: {self.due_date.strftime('%Y-%m-%d')})"
    

    def __eq__(self, other):
        if isinstance(other, Todo):
            return self.description == other.description and self.due_date == other.due_date
        elif isinstance(other, str):
            return self.description == other
        return False
    
    # 🔑 When Python SCOWLS... Use this
    def __hash__(self) -> int:
        return hash((self.description, self.due_date))


    @property
    def priority_score(self) -> int:
        # Convert date straight to integer timestamp — zero Python overhead
        return int(self.due_date.timestamp())