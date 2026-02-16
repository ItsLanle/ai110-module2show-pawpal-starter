"""
PawPal+ CLI Test Script
Tests the pet care planning system by creating owners, pets, tasks, and generating schedules.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    print("=" * 60)
    print("🐾 Welcome to PawPal+ Pet Care Planning System 🐾")
    print("=" * 60)
    print()

    # Create an Owner
    owner = Owner(
        name="Sarah Johnson",
        available_min=120  # 2 hours available today
    )
    owner.update_preferences({"priority_focus": "health", "preferred_time": "morning"})
    print(f"✅ Created Owner: {owner.name}")
    print(f"   Available time: {owner.available_minutes} minutes")
    print()

    # Create Pets
    pet1 = Pet(
        name="Max",
        species="Dog",
        age=5,
        special_needs=["Hip dysplasia", "Medication at 8am"]
    )

    pet2 = Pet(
        name="Whiskers",
        species="Cat",
        age=3,
        special_needs=["Indoor only"]
    )

    # Add pets to owner
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    print(f"✅ Created Pets: {pet1.name} (Dog) and {pet2.name} (Cat)")
    print()

    # ---------------------------------------------------------
    # Create Tasks OUT OF ORDER by time (to test sorting)
    # ---------------------------------------------------------

    # Create Tasks for Max (Dog)
    task1 = Task(
        name="Morning Walk",
        duration=30,
        priority=5,
        category="Exercise",
        required=True,
        frequency="daily",
        time="09:30"
    )

    task2 = Task(
        name="Give Medication",
        duration=5,
        priority=5,
        category="Health",
        required=True,
        frequency="daily",
        time="08:00"
    )

    task3 = Task(
        name="Play Fetch",
        duration=20,
        priority=3,
        category="Play",
        required=False,
        frequency="daily",
        time="16:00"
    )

    task4 = Task(
        name="Grooming",
        duration=45,
        priority=2,
        category="Hygiene",
        required=False,
        frequency="weekly",
        time="14:00"
    )

    # Add tasks to Max (intentionally mixed order)
    pet1.add_task(task3)
    pet1.add_task(task1)
    pet1.add_task(task4)
    pet1.add_task(task2)

    # Create Tasks for Whiskers (Cat)
    task5 = Task(
        name="Feed Breakfast",
        duration=10,
        priority=5,
        category="Feeding",
        required=True,
        frequency="daily",
        time="07:30"
    )

    task6 = Task(
        name="Clean Litter Box",
        duration=15,
        priority=4,
        category="Hygiene",
        required=True,
        frequency="daily",
        time="09:30"  # Intentional conflict
    )

    task7 = Task(
        name="Interactive Play",
        duration=25,
        priority=3,
        category="Play",
        required=False,
        frequency="daily",
        time="18:00"
    )

    # Add tasks to Whiskers (mixed order)
    pet2.add_task(task7)
    pet2.add_task(task5)
    pet2.add_task(task6)

    print(f"✅ Added {len(pet1.get_tasks())} tasks to {pet1.name}")
    print(f"✅ Added {len(pet2.get_tasks())} tasks to {pet2.name}")
    print()

    # ---------------------------------------------------------
    # TEST: Show all tasks sorted by time (before scheduling)
    # ---------------------------------------------------------
    scheduler = Scheduler(owner)

    print("=" * 60)
    print("🕒 ALL TASKS SORTED BY TIME (TEST)")
    print("=" * 60)

    sorted_tasks = scheduler.sort_by_time()

    for task in sorted_tasks:
        print(f"{task.time} - {task.name} ({task.pet.name})")

    print()

    # ---------------------------------------------------------
    # TEST: CHECKING FOR TIME CONFLICTS
    # ---------------------------------------------------------

    print("=" * 60)
    print("🚨 CHECKING FOR TIME CONFLICTS")
    print("=" * 60)

    conflicts = scheduler.detect_time_conflicts()

    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("✅ No time conflicts detected.")

    print()

    # ---------------------------------------------------------
    # TEST: Filtering by pet
    # ---------------------------------------------------------
    print("=" * 60)
    print("🐶 FILTER: TASKS FOR MAX ONLY")
    print("=" * 60)

    max_tasks = [t for t in scheduler.tasks if t.pet.name == "Max"]
    for task in scheduler.sort_by_time(max_tasks):
        print(f"{task.time} - {task.name}")

    print()

    # ---------------------------------------------------------
    # TEST: Filtering required tasks only
    # ---------------------------------------------------------
    print("=" * 60)
    print("🔴 FILTER: REQUIRED TASKS ONLY")
    print("=" * 60)

    required_tasks = [t for t in scheduler.tasks if t.required]
    for task in scheduler.sort_by_time(required_tasks):
        print(f"{task.time} - {task.name} ({task.pet.name})")

    print()

    # ---------------------------------------------------------
    # Generate Daily Plan
    # ---------------------------------------------------------
    print("=" * 60)
    print("📅 GENERATING TODAY'S SCHEDULE")
    print("=" * 60)
    print()

    daily_plan = scheduler.generate_daily_plan()
    summary = scheduler.get_plan_summary()

    # Display Today's Schedule
    print("🗓️  TODAY'S SCHEDULE (Sorted by Time)")
    print("-" * 60)
    print(f"Owner: {owner.name}")
    print(f"Available Time: {owner.available_minutes} minutes")
    print(f"Total Scheduled Time: {summary['total_time']} minutes")
    print(f"Tasks Scheduled: {summary['task_count']}")
    print()

    if daily_plan:
        print("📋 Scheduled Tasks:")
        print()
        for i, task in enumerate(daily_plan, 1):
            required_badge = "🔴 REQUIRED" if task.required else "🟢 Optional"
            print(f"{i}. {task.time} - {task.name} ({task.pet.name})")
            print(f"   Duration: {task.duration} min")
            print(f"   Category: {task.category} | Priority: {task.priority}/5")
            print(f"   Status: {required_badge}")
            print()
    else:
        print("⚠️  No tasks scheduled (not enough time available)")
        print()

    # ---------------------------------------------------------
    # Show excluded tasks if any
    # ---------------------------------------------------------
    if summary['tasks_excluded']:
        print("⏸️  TASKS NOT SCHEDULED (Insufficient Time):")
        print("-" * 60)
        excluded_task_objects = [task for task in scheduler.tasks if task not in daily_plan]
        for task in excluded_task_objects:
            print(f"   • {task.time} - {task.name} ({task.duration} min)")
        print()

    # ---------------------------------------------------------
    # Show pet details
    # ---------------------------------------------------------
    print("=" * 60)
    print("🐾 PET DETAILS")
    print("=" * 60)
    for pet in owner.get_pets():
        print(f"\n{pet.name} ({pet.species}, {pet.age} years old)")
        if pet.special_needs:
            print(f"   Special Needs: {', '.join(pet.special_needs)}")
        print(f"   Total Tasks: {len(pet.get_tasks())}")
        completed = sum(1 for t in pet.get_tasks() if t.completion_status)
        print(f"   Completed Today: {completed}/{len(pet.get_tasks())}")

    print()

    # ---------------------------------------------------------
    # TESTING AUTO-RESCHEDULE (FIXED LOCATION)
    # ---------------------------------------------------------
    print("\n🔁 TESTING AUTO-RESCHEDULE")
    print("=" * 60)

    print("Before:", len(pet.get_tasks()), "tasks")

    new_task = task1.mark_complete()

    print("After:", len(pet.get_tasks()), "tasks")

    if new_task:
        print("New task created:", new_task)

    print()
    print("=" * 60)
    print("✨ Schedule generation complete! ✨")
    print("=" * 60)


if __name__ == "__main__":
    main()
