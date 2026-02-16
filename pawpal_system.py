"""
PawPal+ Pet Care Planning System

This module contains the core classes for managing pet care schedules,
including owners, pets, tasks, and a scheduler for generating daily plans.
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timedelta


class Owner:
    """
    Represents a pet owner with available time and preferences.

    Manages a collection of pets and tracks the owner's available time
    for pet care activities.
    """

    def __init__(self, name: str, available_min: int):
        """Initialize Owner with name and available minutes."""
        self.name: str = name
        self.available_minutes: int = available_min
        self.preferences: dict = {}
        self.pets: list[Pet] = []

    def add_pet(self, pet: 'Pet') -> None:
        """Add a pet to the owner's collection."""
        if pet not in self.pets:
            self.pets.append(pet)
            pet.owner = self

    def remove_pet(self, pet: 'Pet') -> None:
        """Remove a pet from the owner's collection."""
        if pet in self.pets:
            self.pets.remove(pet)
            pet.owner = None

    def get_available_time(self) -> int:
        """Return the owner's available time in minutes."""
        return self.available_minutes

    def update_preferences(self, preferences: dict) -> None:
        """Update the owner's preference dictionary."""
        self.preferences.update(preferences)

    def get_all_tasks(self) -> list['Task']:
        """Return a list of all tasks across the owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_pets(self) -> list['Pet']:
        """Return a copy of the owner's pet list."""
        return self.pets.copy()

    def __str__(self) -> str:
        """Return a string describing the owner."""
        pet_count = len(self.pets)
        pet_word = "pet" if pet_count == 1 else "pets"
        return f"Owner: {self.name} | Available Time: {self.available_minutes}min | {pet_count} {pet_word}"


@dataclass
class Pet:
    """
    Represents a pet with basic information and special needs.

    Tracks pet details including species, age, and any special care requirements.
    """
    name: str
    species: str
    age: int
    special_needs: list[str] = field(default_factory=list)
    owner: Optional['Owner'] = None
    tasks: list['Task'] = field(default_factory=list)

    def add_special_need(self, need: str) -> None:
        """Add a special care need for the pet."""
        if need not in self.special_needs:
            self.special_needs.append(need)

    def add_task(self, task: 'Task') -> None:
        """Add a Task to the pet's tasks list."""
        if task not in self.tasks:
            self.tasks.append(task)
            task.pet = self

    def remove_task(self, task: 'Task') -> None:
        """Remove a Task from the pet's tasks list."""
        if task in self.tasks:
            self.tasks.remove(task)
            if task.pet == self:
                task.pet = None

    def get_care_requirements(self) -> dict:
        """Return basic care info and task count for the pet."""
        return {
            'name': self.name,
            'species': self.species,
            'age': self.age,
            'special_needs': self.special_needs.copy(),
            'task_count': len(self.tasks)
        }

    def get_tasks(self) -> list['Task']:
        """Return a copy of the pet's task list."""
        return self.tasks.copy()

    def __str__(self) -> str:
        """Return a string describing the pet."""
        task_count = len(self.tasks)
        special_needs_str = f" | Special needs: {len(self.special_needs)}" if self.special_needs else ""
        return f"{self.name} ({self.species}, {self.age} years old) | Tasks: {task_count}{special_needs_str}"


@dataclass
class Task:
    """
    Represents a pet care task with duration, priority, category, and time.

    Tasks can be required or optional and may be associated with a specific pet.
    The time attribute (format "HH:MM") allows time-based scheduling.
    """
    name: str
    duration: int
    priority: int  # 1-5 scale
    category: str
    required: bool
    frequency: str = "daily"
    time: Optional[str] = None  # Scheduled time in "HH:MM" format
    completion_status: bool = False
    pet: Optional[Pet] = None
    due_date: Optional[datetime] = None

    def is_required(self) -> bool:
        """Return True if the task is required, else False."""
        return self.required

    def get_priority(self) -> int:
        """Return the task's priority level (1-5)."""
        return self.priority

    def set_priority(self, value: int) -> None:
        """Set the task's priority, validating it's between 1 and 5."""
        if 1 <= value <= 5:
            self.priority = value
        else:
            raise ValueError("Priority must be between 1 and 5")

    def mark_complete(self) -> Optional['Task']:
        """
        Mark the task as complete.
        If the task is recurring (daily or weekly),
        automatically create and attach the next occurrence.
        Returns the new task if created.
        """
        if self.completion_status:
            return None  # Prevent double completion

        self.completion_status = True

        # Only reschedule recurring tasks
        if self.frequency not in ("daily", "weekly"):
            return None

        # Determine next due date
        if not self.due_date:
            next_due = datetime.now()
        else:
            next_due = self.due_date

        if self.frequency == "daily":
            next_due += timedelta(days=1)
        elif self.frequency == "weekly":
            next_due += timedelta(weeks=1)

        # Create new task instance
        new_task = Task(
            name=self.name,
            duration=self.duration,
            priority=self.priority,
            category=self.category,
            required=self.required,
            frequency=self.frequency,
            time=self.time,
            due_date=next_due
        )

    # Attach to same pet
    if self.pet:
        self.pet.add_task(new_task)
    return new_task


    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.completion_status = False

    def __str__(self) -> str:
        """Return a string describing the task."""
        pet_info = f" for {self.pet.name}" if self.pet else ""
        time_info = f" @ {self.time}" if self.time else ""
        req_status = "(Required)" if self.required else "(Optional)"
        completion = "Completed" if self.completion_status else "Pending"
        return (
            f"{self.name}{pet_info}{time_info} - "
            f"{self.duration}min, Priority: {self.priority}/5 "
            f"{req_status} [{completion}]"
        )

    def __lt__(self, other: 'Task') -> bool:
        """
        Compare tasks for sorting:
        Required tasks come first,
        then higher priority tasks.
        """
        if self.required != other.required:
            return self.required
        return self.priority > other.priority

    def complete_and_reschedule(self) -> Optional['Task']:
        """Marks the task complete and creates a new instance
        if the task is recurring (daily or weekly)."""
        self.mark_complete()

        if self.frequency not in ("daily", "weekly"):
            return None

        # Determine next due date
        if not self.due_date:
            next_due = datetime.now()
        else:
            next_due = self.due_date

        if self.frequency == "daily":
            next_due += timedelta(days=1)
        elif self.frequency == "weekly":
            next_due += timedelta(weeks=1)

        # Create new task instance
        new_task = Task(
            name=self.name,
            duration=self.duration,
            priority=self.priority,
            category=self.category,
            required=self.required,
            frequency=self.frequency,
            time=self.time,
            due_date=next_due
        )

        # Attach to same pet
        if self.pet:
            self.pet.add_task(new_task)

        return new_task


class Scheduler:
    """
    Manages scheduling of pet care tasks for an owner.

    Generates optimized daily plans based on available time, task priorities,
    and time-based scheduling when provided.
    """

    def __init__(self, owner: Owner):
        """Initialize Scheduler for the given Owner."""
        self.owner: Owner = owner
        self.pets: list[Pet] = owner.get_pets()
        self.tasks: list[Task] = self.get_all_tasks()
        self.daily_plan: list[Task] = []

    def get_all_tasks(self) -> list[Task]:
        """Always fetch the latest tasks from the owner."""
        return self.owner.get_all_tasks()


    def prioritize_tasks(self) -> list[Task]:
        """Return tasks sorted by requirement and priority."""
        return sorted(self.get_all_tasks())


    def sort_by_time(self, tasks: Optional[list[Task]] = None) -> list[Task]:
        """
        Sort tasks by their time attribute ("HH:MM").

        Tasks without a time are placed at the end.
        Uses Python's sorted() with a lambda key function.
        """
        task_list = tasks if tasks is not None else self.get_all_tasks()

        # Helper function to convert "HH:MM" to total minutes
        def time_to_minutes(time_str: str) -> int:
            hours, minutes = map(int, time_str.split(":"))
            return hours * 60 + minutes

        return sorted(
            task_list,
            key=lambda t: (
                t.time is None,  # Timed tasks first, untimed last
                time_to_minutes(t.time) if t.time else float("inf")
            )
        )

    def calculate_total_time(self, tasks: Optional[list[Task]] = None) -> int:
        """Calculate total duration (minutes) for given tasks or the daily plan."""
        task_list = tasks if tasks is not None else self.daily_plan
        return sum(task.duration for task in task_list)

    def generate_daily_plan(self) -> list[Task]:
        """
        Generate a daily task plan honoring required tasks,
        priority order, available time limits,
        and finally sorting by scheduled time.
        """
        prioritized = self.prioritize_tasks()
        available_time = self.owner.get_available_time()
        self.daily_plan = []
        total_time = 0

        # First pass: add all required tasks
        required_tasks = [t for t in prioritized if t.required]
        required_time = self.calculate_total_time(required_tasks)

        if required_time > available_time:
            raise ValueError(
                f"Required tasks ({required_time}min) exceed available time ({available_time}min)"
            )

        self.daily_plan.extend(required_tasks)
        total_time = required_time

        # Second pass: add optional tasks in priority order
        optional_tasks = [t for t in prioritized if not t.required]
        for task in optional_tasks:
            if total_time + task.duration <= available_time:
                self.daily_plan.append(task)
                total_time += task.duration

        # Final step: sort selected tasks by time (if provided)
        self.daily_plan = self.sort_by_time(self.daily_plan)

        return self.daily_plan

    def get_plan_summary(self) -> dict:
        """Return a summary dict for the current daily plan."""
        total_time = self.calculate_total_time()
        task_count = len(self.daily_plan)

        tasks_included = [task.name for task in self.daily_plan]
        tasks_excluded = [
            task.name for task in self.get_all_tasks()
            if task not in self.daily_plan
]

        return {
            'total_time': total_time,
            'task_count': task_count,
            'tasks_included': tasks_included,
            'tasks_excluded': tasks_excluded
        }

    def detect_time_conflicts(self, tasks: Optional[list[Task]] = None) -> list[str]:
         """
    Detect tasks scheduled at the same time.

    Args:
        tasks (Optional[list[Task]]): A list of tasks to check. Defaults to all tasks.

    Returns:
        list[str]: A list of warning messages indicating conflicts.
    """
        task_list = tasks if tasks is not None else self.get_all_tasks()
        warnings = []

        time_map = {}

        for task in task_list:
            if not task.time:
                continue

            if task.time not in time_map:
                time_map[task.time] = [task]
            else:
                time_map[task.time].append(task)

        for time, tasks_at_time in time_map.items():
            if len(tasks_at_time) > 1:
                task_names = ", ".join(
                    f"{t.name} ({t.pet.name})" for t in tasks_at_time
                )
                warnings.append(f"⚠️ Conflict at {time}: {task_names}")

        return warnings
