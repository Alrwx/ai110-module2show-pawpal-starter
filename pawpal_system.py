from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class Task:
    description: str
    time: str 
    frequency: str = "once" 
    priority: str = "medium" 
    duration_minutes: int = 15
    completed: bool = False
    pet_name: str = ""

    def mark_complete(self):
        self.completed = True

    def __str__(self):
        status = "done" if self.completed else "pending"
        return f"[{status}] {self.time} - {self.description} ({self.priority}, {self.duration_minutes}min)"


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, description: str):
        self.tasks = [t for t in self.tasks if t.description != description]

    def get_pending_tasks(self):
        return [t for t in self.tasks if not t.completed]

    def __str__(self):
        return f"{self.name} ({self.species}, age {self.age}) — {len(self.tasks)} tasks"


@dataclass
class Owner:
    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def remove_pet(self, pet_name: str):
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_all_tasks(self):
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def find_pet(self, pet_name: str) -> Optional[Pet]:
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None

    def __str__(self):
        pet_names = ", ".join(p.name for p in self.pets) if self.pets else "no pets"
        return f"{self.name} — pets: {pet_names}"


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self):
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: Optional[list] = None):
        if tasks is None:
            tasks = self.get_all_tasks()
        return sorted(tasks, key=lambda t: t.time)

    def sort_by_priority(self, tasks: Optional[list] = None):
        priority_order = {"high": 0, "medium": 1, "low": 2}
        if tasks is None:
            tasks = self.get_all_tasks()
        return sorted(tasks, key=lambda t: priority_order.get(t.priority, 1))

    def filter_by_status(self, completed: bool, tasks: Optional[list] = None):
        if tasks is None:
            tasks = self.get_all_tasks()
        return [t for t in tasks if t.completed == completed]

    def filter_by_pet(self, pet_name: str, tasks: Optional[list] = None):
        """quick helper to show only tasks for one pet."""
        if tasks is None:
            tasks = self.get_all_tasks()
        return [t for t in tasks if t.pet_name == pet_name]

    def detect_conflicts(self, tasks: Optional[list] = None):
        """spots tasks that land on the same time and returns a heads-up."""
        if tasks is None:
            tasks = self.get_all_tasks()
        conflicts = []
        seen = {}
        for task in tasks:
            if task.time in seen:
                conflicts.append(
                    f"conflict: '{task.description}' ({task.pet_name}) and "
                    f"'{seen[task.time].description}' ({seen[task.time].pet_name}) "
                    f"are both at {task.time}"
                )
            else:
                seen[task.time] = task
        return conflicts

    def mark_task_complete(self, pet_name: str, description: str):
        """marks a task done and spins up the next one if it repeats."""
        pet = self.owner.find_pet(pet_name)
        if pet is None:
            return None

        for task in pet.tasks:
            if task.description == description and not task.completed:
                task.mark_complete()
                new_task = self._create_next_occurrence(task)
                if new_task:
                    pet.add_task(new_task)
                return task
        return None

    def _create_next_occurrence(self, task: Task):
        if task.frequency == "once":
            return None

        today = datetime.now()
        if task.frequency == "daily":
            next_date = today + timedelta(days=1)
        elif task.frequency == "weekly":
            next_date = today + timedelta(weeks=1)
        else:
            return None

        return Task(
            description=task.description,
            time=task.time,
            frequency=task.frequency,
            priority=task.priority,
            duration_minutes=task.duration_minutes,
            completed=False,
            pet_name=task.pet_name,
        )

    def get_todays_schedule(self):
        pending = self.filter_by_status(completed=False)
        return self.sort_by_time(pending)

    def generate_schedule_summary(self):
        schedule = self.get_todays_schedule()
        conflicts = self.detect_conflicts(schedule)

        lines = []
        lines.append(f"schedule for {self.owner.name}:")
        lines.append("-" * 40)

        if not schedule:
            lines.append("no tasks scheduled!")
        else:
            for task in schedule:
                lines.append(f"  {task}")

        if conflicts:
            lines.append("")
            lines.append("warnings:")
            for c in conflicts:
                lines.append(f"  {c}")

        return "\n".join(lines)
