import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Initialize Owner once per session
if 'owner' not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_min=120)

# Initialize the list of pets in session state
if 'pets' not in st.session_state:
    st.session_state.pets = []

# Initialize the list of tasks in session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

owner = st.session_state.owner

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("🐾 Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)

if st.button("Add pet"):
    # Create a new Pet instance and add it to the owner
    pet = Pet(name=pet_name, species=species, age=age)
    owner.add_pet(pet)
    st.session_state.pets.append(pet)
    st.success(f"✓ Added {pet_name} the {species} to {owner.name}'s pets!")

if st.session_state.pets:
    st.markdown("**Your Pets:**")
    for pet in st.session_state.pets:
        st.write(f"• {pet}")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("📋 Add a Task")
if not st.session_state.pets:
    st.warning("Add a pet first to assign tasks.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        task_name = st.text_input("Task name", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority (1-5)", [1, 2, 3, 4, 5], index=4)

    category = st.selectbox("Category", ["feeding", "exercise", "grooming", "medical", "play", "other"])
    required = st.checkbox("Required task", value=True)
    selected_pet_name = st.selectbox("Assign to pet", [p.name for p in st.session_state.pets])

    if st.button("Add task"):
        # Find the selected pet and create the task
        selected_pet = next(p for p in st.session_state.pets if p.name == selected_pet_name)
        task = Task(
            name=task_name,
            duration=int(duration),
            priority=int(priority),
            category=category,
            required=required,
            pet=selected_pet
        )
        # Add task to pet using the Pet.add_task method
        selected_pet.add_task(task)
        st.session_state.tasks.append(task)
        st.success(f"✓ Added '{task_name}' to {selected_pet_name}!")

if st.session_state.tasks:
    st.markdown("**Current Tasks:**")
    for task in st.session_state.tasks:
        st.write(f"• {task}")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("📅 Generate Daily Schedule")
st.caption("Create an optimized schedule based on available time and task priorities.")

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("Add tasks first before generating a schedule.")
    else:
        try:
            # Create a scheduler for the owner
            scheduler = Scheduler(owner)
            
            # Generate the daily plan
            daily_plan = scheduler.generate_daily_plan()
            
            # Get a summary of the plan
            summary = scheduler.get_plan_summary()
            
            st.success("✓ Schedule generated successfully!")
            
            st.markdown("### Daily Plan Summary")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Time Required", f"{summary['total_time']} min")
            with col2:
                st.metric("Tasks Scheduled", summary['task_count'])
            
            st.markdown("### Tasks in Schedule")
            if daily_plan:
                for i, task in enumerate(daily_plan, 1):
                    status = "✓ Required" if task.required else "○ Optional"
                    st.write(f"{i}. {task.name} ({task.duration} min) - Priority: {task.priority}/5 {status}")
            else:
                st.info("No tasks fit in the available time.")
            
            if summary['tasks_excluded']:
                st.markdown("### Tasks Not Scheduled")
                st.warning(f"Could not fit: {', '.join(summary['tasks_excluded'])}")
        except ValueError as e:
            st.error(f"⚠️ Scheduling error: {e}")
