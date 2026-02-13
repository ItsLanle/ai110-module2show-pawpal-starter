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

    # Create Tasks for Max (Dog)
    task1 = Task(
        name="Morning Walk",
        duration=30,
        priority=5,
        category="Exercise",
        required=True,
        frequency="daily"
    )

    task2 = Task(
        name="Give Medication",
        duration=5,
        priority=5,
        category="Health",
        required=True,
        frequency="daily"
    )

    task3 = Task(
        name="Play Fetch",
        duration=20,
        priority=3,
        category="Play",
        required=False,
        frequency="daily"
    )

    task4 = Task(
        name="Grooming",
        duration=45,
        priority=2,
        category="Hygiene",
        required=False,
        frequency="weekly"
    )

    # Add tasks to Max
    pet1.add_task(task1)
    pet1.add_task(task2)
    pet1.add_task(task3)
    pet1.add_task(task4)

    # Create Tasks for Whiskers (Cat)
    task5 = Task(
        name="Feed Breakfast",
        duration=10,
        priority=5,
        category="Feeding",
        required=True,
        frequency="daily"
    )

    task6 = Task(
        name="Clean Litter Box",
        duration=15,
        priority=4,
        category="Hygiene",
        required=True,
        frequency="daily"
    )

    task7 = Task(
        name="Interactive Play",
        duration=25,
        priority=3,
        category="Play",
        required=False,
        frequency="daily"
    )

    # Add tasks to Whiskers
    pet2.add_task(task5)
    pet2.add_task(task6)
    pet2.add_task(task7)

    print(f"✅ Added {len(pet1.get_tasks())} tasks to {pet1.name}")
    print(f"✅ Added {len(pet2.get_tasks())} tasks to {pet2.name}")
    print()

    # Create Scheduler and generate daily plan
    print("=" * 60)
    print("📅 GENERATING TODAY'S SCHEDULE")
    print("=" * 60)
    print()

    scheduler = Scheduler(owner)
    daily_plan = scheduler.generate_daily_plan()

    # Get plan summary
    summary = scheduler.get_plan_summary()

    # Display Today's Schedule
    print("🗓️  TODAY'S SCHEDULE")
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
            print(f"{i}. {task.name} - {task.duration} min")
            print(f"   Category: {task.category} | Priority: {task.priority}/5")
            print(f"   Status: {required_badge}")
            print()
    else:
        print("⚠️  No tasks scheduled (not enough time available)")
        print()

    # Show excluded tasks if any
    if summary['tasks_excluded']:
        print("⏸️  TASKS NOT SCHEDULED (Insufficient Time):")
        print("-" * 60)
        # Get the actual Task objects that were excluded
        excluded_task_objects = [task for task in scheduler.tasks if task not in daily_plan]
        for task in excluded_task_objects:
            print(f"   • {task.name} ({task.duration} min) - Priority {task.priority}/5")
        print()

    # Show pet details
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
    print("=" * 60)
    print("✨ Schedule generation complete! ✨")
    print("=" * 60)


if __name__ == "__main__":
    main()
