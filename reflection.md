# PawPal+ Project Reflection

## 1. System Design
- The 3 core actions a user should be able to perform are allowing the user to enter basic information, allowing the user to add and edit tasks, and allowing the user to generate a daily plan based off the contraints they have.
**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The PawPal+ system consists of four main classes:

Owner - Represents the pet owner with time constraints and preferences. Responsibilities include managing a collection of pets, tracking available time (in minutes), and storing user preferences for scheduling. Acts as the primary user entity in the system.

Pet - Represents an individual pet with basic information and care needs. Responsibilities include storing pet details (name, species, age) and managing a list of special needs that affect care requirements. Implemented as a dataclass for simplicity.

Task - Represents a care activity with scheduling metadata. Responsibilities include storing task details (name, duration, category), maintaining priority levels (1-5), and indicating whether the task is required. Supports comparison operations for priority-based sorting. Implemented as a dataclass and optionally linked to a specific pet.

Scheduler - The central coordinator that connects all components. Responsibilities include managing the owner's schedule, organizing tasks based on priority and time constraints, and generating an optimized daily care plan that respects the owner's available minutes and pet needs.

Key relationships: Owner owns multiple Pets (1-to-many), and Scheduler uses Owner, Pets, and Tasks to create scheduling plans.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, several design changes were made during implementation to address critical relationship and logic bottlenecks:

1. **Added Bidirectional Owner-Pet Relationship**: Initially, the Pet class had no reference back to its Owner. I added an `owner` field to Pet so that a pet can identify which owner it belongs to. This enables validation (e.g., preventing tasks for pets the owner doesn't have) and allows direct pet-to-owner navigation.

2. **Added Bidirectional Task-Pet Tracking**: The original design allowed Task to reference Pet, but Pet had no way to access its tasks. I added a `tasks` field to Pet, creating a bidirectional association. This allows querying "what tasks are associated with this pet?" which is essential for care planning and pet-specific task management.

3. **Removed Redundant Scheduler.pets**: Initially, Scheduler maintained its own `self.pets` list separate from `self.owner.pets`. This created data consistency issues. I removed the redundant list and now Scheduler accesses pets through `self.owner.pets`, establishing a single source of truth.

4. **Two-Pass Scheduling Algorithm**: The initial generate_daily_plan() stub gave no guidance on implementation. I implemented a constraint-aware two-pass algorithm: first schedule all required tasks (with validation that they fit), then greedily add optional tasks by priority. This ensures feasibility and prevents over-scheduling.

5. **Enhanced Validation**: Added pet ownership validation in `add_task()` to prevent orphaned tasks, and priority range validation in `set_priority()` to prevent invalid states.

These changes were made because the original design had information asymmetry and lacked constraint enforcement, which would cause runtime errors or impossible schedules. The bidirectional relationships create a more robust model that prevents invalid states at insertion time rather than discovery time.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    The scheduler first respects hard constraints like required tasks and the owner’s available time, ensuring essential pet care is never missed. Optional tasks are added based on priority, and tasks with specific times are scheduled accordingly. Owner preferences (e.g., focus on health or preferred time of day) are considered but do not override critical constraints. This approach balances safety, efficiency, and flexibility.
- How did you decide which constraints mattered most?
    The scheduler focuses first on hard constraints (required tasks and time), then soft constraints (priority, scheduled time, preferences). This ensures safety and usability while still giving flexibility for optional activities.

    Required tasks first: Safety and health-related tasks (e.g., medication, feeding) are critical, so they are always scheduled before optional activities.

    Time limitations next: The owner’s daily availability is a hard limit, so no tasks are scheduled beyond the total available minutes.
    
    Priority within optional tasks: Among tasks that aren’t strictly required, the scheduler uses the priority rating to decide what to include if time is limited.

    Scheduled times as a tie-breaker: When multiple tasks compete, tasks with a specific time take precedence in the daily plan to preserve consistency with the owner’s schedule.

    Preferences are secondary: Preferences inform the scheduler but do not override hard constraints like required tasks or available time.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.   
    One tradeoff the scheduler currently makes is that it only detects exact time matches for tasks when checking conflicts. 
    This means it does not detect overlapping durations—for example, a 30-minute walk starting at 09:00 and a 20-minute feeding at 09:15 would not be flagged as a conflict. 
    This simplifies the algorithm and makes it faster, but it may miss some practical scheduling conflicts.
- Why is that tradeoff reasonable for this scenario?
    The tradeoff prioritizes simplicity, clarity, and usability over exhaustive conflict detection, which is appropriate given the scope of the PawPal+ app.



---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    AI tools were used throughout the project for design brainstorming, debugging, and refactoring. They helped generate example class structures, suggest methods for sorting and scheduling tasks, and troubleshoot errors in the CLI script.

- What kinds of prompts or questions were most helpful?
    Prompts that were most helpful included asking for step-by-step Python implementations, requests to “rewrite code with all comments intact,” and clarifying how to automatically reschedule recurring tasks.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    One moment I didn’t accept an AI suggestion as-is was when it proposed a “Pythonic” one-liner to sort tasks. While the code was technically correct, it was harder for a human reader to follow, especially with multiple conditions like required status and priority. 
- How did you evaluate or verify what the AI suggested?
    I evaluated the suggestion by manually tracing the logic on sample tasks and comparing the output to my existing method to ensure it maintained the correct order and readability. I ultimately kept my original version for clarity.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    I tested several key behaviors of the scheduler:
    Task sorting by time – to ensure tasks appear in chronological order regardless of the order they were added.
    Time conflict detection – to verify that overlapping tasks were flagged correctly.
    Filtering tasks – by pet and by required status, to confirm accurate selection.
    Daily plan generation – to make sure required tasks fit within the owner's available time and optional tasks were added when possible.
    Auto-rescheduling recurring tasks – to ensure “daily” and “weekly” tasks generate a new instance after completion.
    
- Why were these tests important?
    These tests were important because they confirmed that the scheduler reliably prioritizes tasks, respects time limits, and handles recurring events — all core functionalities of the system.
**b. Confidence**

- How confident are you that your scheduler works correctly?
    I am confident that the scheduler works correctly for the scenarios tested, including out-of-order tasks, required vs optional tasks, and time conflicts.

- What edge cases would you test next if you had more time?
    If I had more time, I would test additional edge cases such as:
    Tasks that partially overlap in duration, not just exact start times.
    Zero-duration tasks or tasks longer than the owner's available time.
    Pets with no tasks or an owner with no available time.
    Simultaneous recurring tasks to check for proper scheduling of multiple next occurrences.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
