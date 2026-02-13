"""
PawPal+ Pet Care Planning System

This module contains the core classes for managing pet care schedules,
including owners, pets, tasks, and a scheduler for generating daily plans.
"""

from dataclasses import dataclass, field
from typing import Optional


class Owner:
    """
    Represents a pet owner with available time and preferences.

    Manages a collection of pets and tracks the owner's available time
    for pet care activities.
    """

    def __init__(self, name: str, available_min: int):
        """
        Initialize an Owner with name and available minutes.

        Args:
            name: The owner's name
            available_min: Available minutes per day for pet care
        """
        self.name: str = name
        self.available_minutes: int = available_min
        self.preferences: dict = {}
        self.pets: list[Pet] = []

    def add_pet(self, pet: 'Pet') -> None:
        """
        Add a pet to the owner's collection.

        Args:
            pet: The Pet object to add
        """
        if pet not in self.pets:
            self.pets.append(pet)
            pet.owner = self

    def remove_pet(self, pet: 'Pet') -> None:
        """
        Remove a pet from the owner's collection.

        Args:
            pet: The Pet object to remove
        """
        if pet in self.pets:
            self.pets.remove(pet)
            pet.owner = None

    def get_available_time(self) -> int:
        """
        Get the owner's available time in minutes.

        Returns:
            Available minutes for pet care
        """
        return self.available_minutes

    def update_preferences(self, preferences: dict) -> None:
        """
        Update the owner's preferences for pet care.

        Args:
            preferences: Dictionary of preference key-value pairs
        """
        self.preferences.update(preferences)

    def get_all_tasks(self) -> list['Task']:
        """
        Get all tasks from all pets owned by this owner.

        Returns:
            List of all tasks across all pets
        """
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_pets(self) -> list['Pet']:
        """
        Get the list of pets owned by this owner.

        Returns:
            List of Pet objects
        """
        return self.pets.copy()

    def __str__(self) -> str:
        """
        Return a string representation of the owner.

        Returns:
            String describing the owner
        """
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
        """
        Add a special need or care requirement for the pet.

        Args:
            need: Description of the special need
        """
        if need not in self.special_needs:
            self.special_needs.append(need)

    def add_task(self, task: 'Task') -> None:
        """
        Add a task to the pet's task list.

        Args:
            task: The Task object to add
        """
        if task not in self.tasks:
            self.tasks.append(task)
            task.pet = self

    def remove_task(self, task: 'Task') -> None:
        """
        Remove a task from the pet's task list.

        Args:
            task: The Task object to remove
        """
        if task in self.tasks:
            self.tasks.remove(task)
            if task.pet == self:
                task.pet = None

    def get_care_requirements(self) -> dict:
        """
        Get all care requirements for this pet.

        Returns:
            Dictionary with pet info and count of tasks
        """
        return {
            'name': self.name,
            'species': self.species,
            'age': self.age,
            'special_needs': self.special_needs.copy(),
            'task_count': len(self.tasks)
        }

    def get_tasks(self) -> list['Task']:
        """
        Get the list of tasks for this pet.

        Returns:
            List of Task objects
        """
        return self.tasks.copy()

    def __str__(self) -> str:
        """
        Return a string representation of the pet.

        Returns:
            String describing the pet
        """
        task_count = len(self.tasks)
        special_needs_str = f" | Special needs: {len(self.special_needs)}" if self.special_needs else ""
        return f"{self.name} ({self.species}, {self.age} years old) | Tasks: {task_count}{special_needs_str}"


@dataclass
class Task:
    """
    Represents a pet care task with duration, priority, and category.

    Tasks can be required or optional and may be associated with a specific pet.
    """

    name: str
    duration: int
    priority: int  # 1-5 scale
    category: str
    required: bool
    frequency: str = "daily"
    completion_status: bool = False
    pet: Optional[Pet] = None

    def is_required(self) -> bool:
        """
        Check if this task is required.

        Returns:
            True if task is required, False otherwise
        """
        return self.required

    def get_priority(self) -> int:
        """
        Get the priority level of this task.

        Returns:
            Priority value (1-5)
        """
        return self.priority

    def set_priority(self, value: int) -> None:
        """
        Set the priority level for this task.

        Args:
            value: Priority value (1-5)

        Raises:
            ValueError: If priority is not between 1 and 5
        """
        if 1 <= value <= 5:
            self.priority = value
        else:
            raise ValueError("Priority must be between 1 and 5")

    def mark_complete(self) -> None:
        """
        Mark the task as complete.
        """
        self.completion_status = True

    def mark_incomplete(self) -> None:
        """
        Mark the task as incomplete.
        """
        self.completion_status = False

    def __str__(self) -> str:
        """
        Return a string representation of the task.

        Returns:
            String describing the task
        """
        pet_info = f" for {self.pet.name}" if self.pet else ""
        req_status = "(Required)" if self.required else "(Optional)"
        completion = "Completed" if self.completion_status else "Pending"
        return f"{self.name}{pet_info} - {self.duration}min, Priority: {self.priority}/5 {req_status} [{completion}]"

    def __lt__(self, other: 'Task') -> bool:
        """
        Compare tasks for sorting by priority.
        Higher priority comes first (reverse comparison).

        Args:
            other: Another Task object to compare with

        Returns:
            True if this task should come before other in sorted order
        """
        # Required tasks come before optional tasks
        if self.required != other.required:
            return self.required  # Required (True) comes before Optional (False)
        # Higher priority values come first (reverse comparison)
        return self.priority > other.priority


class Scheduler:
    """
    Manages scheduling of pet care tasks for an owner.

    Generates optimized daily plans based on available time, task priorities,
    and pet care requirements.
    """

    def __init__(self, owner: Owner):
        """
        Initialize a Scheduler for a given owner.
        Extracts pets from owner and collects all tasks from all pets.

        Args:
            owner: The Owner object to create schedules for
        """
        self.owner: Owner = owner
        self.pets: list[Pet] = owner.get_pets()
        self.tasks: list[Task] = owner.get_all_tasks()
        self.daily_plan: list[Task] = []

    def get_all_pet_tasks(self) -> list[Task]:
        """
        Retrieve all tasks from the owner's pets.
        
        Aggregates tasks across all pets owned by this owner.

        Returns:
            List of all tasks associated with owner's pets
        """
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def add_task(self, task: Task) -> None:
        """
        Add a task to the scheduler.

        Args:
            task: The Task object to add
            
        Raises:
            ValueError: If task is associated with a pet not owned by this owner
        """
        if task.pet is not None and task.pet not in self.owner.pets:
            raise ValueError(f"Task is for pet {task.pet.name}, which is not owned by {self.owner.name}")
        
        if task not in self.tasks:
            self.tasks.append(task)
            if task.pet:
                task.pet.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """
        Remove a task from the scheduler.

        Args:
            task: The Task object to remove
        """
        if task in self.tasks:
            self.tasks.remove(task)
            if task.pet and task in task.pet.tasks:
                task.pet.tasks.remove(task)

    def prioritize_tasks(self) -> list[Task]:
        """
        Sort and prioritize tasks based on priority level and requirements.

        Returns:
            Sorted list of tasks by priority (highest priority first, required tasks first)
        """
        return sorted(self.tasks, reverse=False)  # __lt__ already implements correct ordering

    def calculate_total_time(self, tasks: Optional[list[Task]] = None) -> int:
        """
        Calculate the total time required for tasks.

        Args:
            tasks: List of tasks to calculate time for. If None, uses daily_plan.

        Returns:
            Total minutes required
        """
        task_list = tasks if tasks is not None else self.daily_plan
        return sum(task.duration for task in task_list)

    def generate_daily_plan(self) -> list[Task]:
        """
        Generate a daily plan of tasks based on priorities and available time.
        
        Includes all required tasks that fit within available time, then optional
        tasks in priority order up to the time limit.

        Returns:
            List of tasks in the daily plan
            
        Raises:
            ValueError: If required tasks exceed available time
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
        
        return self.daily_plan

    def optimize_schedule(self) -> list[Task]:
        """
        Optimize the schedule to maximize high-priority and required tasks within time limit.

        Reorganizes the daily_plan to ensure required tasks are included first,
        followed by highest priority optional tasks that fit within the available time.

        Returns:
            Optimized list of tasks in the daily plan
        """
        # Use generate_daily_plan which already implements optimal scheduling
        return self.generate_daily_plan()

    def get_plan_summary(self) -> dict:
        """
        Get a summary of the current daily plan.

        Returns:
            Dictionary with total_time, task_count, tasks_included, tasks_excluded
        """
        total_time = self.calculate_total_time()
        task_count = len(self.daily_plan)

        # Get tasks included in the plan
        tasks_included = [task.name for task in self.daily_plan]

        # Get tasks excluded from the plan
        tasks_excluded = [task.name for task in self.tasks if task not in self.daily_plan]

        return {
            'total_time': total_time,
            'task_count': task_count,
            'tasks_included': tasks_included,
            'tasks_excluded': tasks_excluded
        }
