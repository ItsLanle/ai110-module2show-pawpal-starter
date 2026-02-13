import sys
from pathlib import Path

# Add parent directory to Python path so we can import pawpal_system
#sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status():
    """Verify that calling mark_complete() changes the task's status."""
    task = Task(
        name="Feed",
        duration=10,
        priority=5,
        category="Feeding",
        required=True
    )
    assert task.completion_status is False
    task.mark_complete()
    assert task.completion_status is True


def test_add_task_increases_pet_task_count():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(
        name="Buddy",
        species="Dog",
        age=3
    )
    initial_count = len(pet.tasks)

    task = Task(
        name="Walk",
        duration=30,
        priority=5,
        category="Exercise",
        required=True
    )
    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1