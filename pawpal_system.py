from dataclasses import dataclass, field
from datetime import date, timedelta

@dataclass
class Task:
    description: str
    time: str
    frequency: str = "once"
    completed: bool = False
    task_date: date = None

    def __post_init__(self):
        if self.task_date is None:
            self.task_date = date.today()


    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True


# Pet、Owner、Scheduler 接着往下写
class Pet:
    def __init__(self, name: str, species: str, age: int):
        self.name = name
        self.species = species
        self.age = age
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        """Add a task to the pet's task list."""
        self.tasks.append(task)

    def get_tasks(self):
        """Return the list of tasks for this pet."""
        return self.tasks
    
class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's list of pets."""
        self.pets.append(pet)

    def get_pets(self):
        """Return the list of pets for this owner."""
        return self.pets
    
class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def build_schedule(self):
        """Build a schedule for the owner's pets based on their tasks."""
        schedule = {}
        for pet in self.owner.get_pets():
            schedule[pet.name] = []
            for task in pet.get_tasks():
                schedule[pet.name].append({
                    "description": task.description,
                    "time": task.time,
                    "frequency": task.frequency,
                    "completed": task.completed
                })
        return schedule
    def sort_by_time(self):
        """Sort the tasks in the schedule by time."""
        all_tasks = []
        for pet in self.owner.get_pets():
            for task in pet.get_tasks():
                all_tasks.append({
                    "pet_name": pet.name,
                    "description": task.description,
                    "time": task.time,
                    "frequency": task.frequency,
                    "completed": task.completed
                })
        all_tasks.sort(key=lambda x: x["time"])
        return all_tasks
    def detect_conflicts(self):
        """Detect any scheduling conflicts among the tasks."""
        sorted_tasks = self.sort_by_time()
        conflicts = []
        for i in range(len(sorted_tasks) - 1):
            current = sorted_tasks[i]
            next_task = sorted_tasks[i + 1]
            if current["time"] == next_task["time"]:
                conflicts.append(
                    f"Conflict at {current['time']}: {current['description']} ({current['pet_name']}) and {next_task['description']} ({next_task['pet_name']})"
                )
        return conflicts
    
    def filter_incomplete_tasks(self):
        """Filter and return only the incomplete tasks."""
        all_tasks = self.sort_by_time()
        result = []
        for task in all_tasks:
            if not task["completed"]:
                result.append(task)
        return result
    
    def filter_by_pet(self, pet_name: str):
        """Filter and return tasks for a specific pet."""
        all_tasks = self.sort_by_time()
        result = []
        for task in all_tasks:
            if task["pet_name"] == pet_name:
                result.append(task)
        return result
    
    def complete_and_reschedule(self, pet, task):
        """Mark a task as complete and reschedule it if it's a recurring task."""
        task.mark_complete()
        if task.frequency == "daily":
            next_date = task.task_date + timedelta(days=1)
        elif task.frequency == "weekly":
            next_date = task.task_date + timedelta(weeks=1)
        else:
            return

        next_task = Task(description=task.description, time=task.time, frequency=task.frequency, task_date=next_date)
        pet.add_task(next_task)
    
